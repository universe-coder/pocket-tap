"""PocketTap window: QR code, network choice, connected phones, log, updates.

Closing the window hides it to the system tray; the server keeps running until
"Quit" in the tray menu. On macOS and Linux closing minimizes the window instead.
"""

import logging
import queue
import sys
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import qrcode
from PIL import Image, ImageDraw, ImageTk

from . import __version__
from .app import describe_device
from .config import load_settings, save_settings
from .i18n import tr
from .net import candidate_ips
from .updates import check_for_update

log = logging.getLogger(__name__)

POLL_MS = 200
UPDATE_EVERY_MS = 24 * 3600 * 1000  # the program may stay in the tray for days
RTL = {"ar"}


class QueueHandler(logging.Handler):
    """Hands log records from any thread to the window."""

    def __init__(self, q):
        super().__init__()
        self.q = q
        self.setFormatter(logging.Formatter("%(asctime)s  %(message)s", "%H:%M:%S"))

    def emit(self, record):
        try:
            self.q.put(("log", self.format(record)))
        except Exception:  # noqa: BLE001 - logging must never raise
            self.handleError(record)


def tray_image(size=64):
    """The phone-with-play-button icon, drawn so no image file has to be shipped."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 64
    d.rounded_rectangle((2 * s, 2 * s, 62 * s, 62 * s), radius=14 * s, fill="#0f1115")
    d.rounded_rectangle((17 * s, 10 * s, 47 * s, 54 * s), radius=6 * s, fill="#1b1f27", outline="#2a303b", width=max(1, int(2 * s)))
    d.ellipse((22 * s, 18 * s, 42 * s, 38 * s), fill="#ff3b3b")
    d.polygon([(29 * s, 23 * s), (29 * s, 33 * s), (37 * s, 28 * s)], fill="white")
    return img


class App:
    def __init__(self, server, clients, token, port, lang, preferred_ip=None):
        self.server, self.clients, self.token, self.port, self.lang = server, clients, token, port, lang
        self.events = queue.Queue()
        self.tray = None
        self.tray_hint_shown = False
        self.update_url = None
        self._shown_clients = None

        handler = QueueHandler(self.events)
        logging.getLogger().addHandler(handler)

        self.root = tk.Tk()
        self.root.title("PocketTap")
        self.root.geometry("880x640")
        self.root.minsize(720, 480)
        try:
            self._icon = ImageTk.PhotoImage(tray_image(64))
            self.root.iconphoto(True, self._icon)
        except tk.TclError:
            pass
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        self._build()
        self.refresh_networks(preferred_ip or load_settings().get("ip"))
        self.show_server_state()
        self._start_tray()
        self.check_updates(quiet=True)
        self.root.after(POLL_MS, self._poll)
        self.root.after(UPDATE_EVERY_MS, self._periodic_update_check)

    def t(self, key, **kw):
        return tr(self.lang, key, **kw)

    # ---- layout -----------------------------------------------------------
    def _build(self):
        style = ttk.Style(self.root)
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Muted.TLabel", foreground="#666")
        style.configure("Ok.TLabel", foreground="#1f8f4e")
        style.configure("Err.TLabel", foreground="#c62828")
        style.configure("Update.TFrame", background="#fff4d6")
        style.configure("Update.TLabel", background="#fff4d6")

        anchor = "e" if self.lang in RTL else "w"
        outer = ttk.Frame(self.root, padding=14)
        outer.pack(fill="both", expand=True)

        head = ttk.Frame(outer)
        head.pack(fill="x")
        ttk.Label(head, text="PocketTap", style="Title.TLabel").pack(side="left")
        ttk.Label(head, text=f"  {__version__}", style="Muted.TLabel").pack(side="left", pady=(6, 0))
        self.status = ttk.Label(head, text="", style="Ok.TLabel")
        self.status.pack(side="right")

        self.update_bar = ttk.Frame(outer, style="Update.TFrame", padding=(10, 6))
        self.update_label = ttk.Label(self.update_bar, text="", style="Update.TLabel")
        self.update_label.pack(side="left")
        ttk.Button(self.update_bar, text=self.t("download"), command=self.open_update).pack(side="right")

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True, pady=(12, 0))
        self.body = body

        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0, 16))
        ttk.Label(left, text=self.t("scan"), wraplength=280, justify="left").pack(anchor=anchor)
        self.qr_label = ttk.Label(left)
        self.qr_label.pack(pady=8)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(left, textvariable=self.url_var, state="readonly", width=40)
        url_entry.pack(fill="x")
        self.copy_btn = ttk.Button(left, text=self.t("copy"), command=self.copy_url)
        self.copy_btn.pack(fill="x", pady=(6, 14))

        ttk.Label(left, text=self.t("network")).pack(anchor=anchor)
        row = ttk.Frame(left)
        row.pack(fill="x", pady=(2, 2))
        self.net_var = tk.StringVar()
        self.net_box = ttk.Combobox(row, textvariable=self.net_var, state="readonly")
        self.net_box.pack(side="left", fill="x", expand=True)
        self.net_box.bind("<<ComboboxSelected>>", lambda e: self.select_network())
        ttk.Button(row, text=self.t("refresh"), command=lambda: self.refresh_networks(self.current_ip)).pack(side="left", padx=(6, 0))
        ttk.Label(left, text=self.t("network_hint"), style="Muted.TLabel", wraplength=280, justify="left").pack(anchor=anchor)

        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text=self.t("connections")).pack(anchor=anchor)
        cols = ("address", "device", "since")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=5)
        for col, width in zip(cols, (130, 220, 80)):
            self.tree.heading(col, text=self.t(f"col_{col}"))
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="x", pady=(2, 0))
        self.empty_label = ttk.Label(right, text=self.t("no_connections"), style="Muted.TLabel")
        self.empty_label.pack(anchor=anchor, pady=(2, 10))

        ttk.Label(right, text=self.t("log")).pack(anchor=anchor)
        self.log_view = ScrolledText(right, height=10, state="disabled", wrap="word", font=("Consolas", 9))
        self.log_view.pack(fill="both", expand=True, pady=(2, 0))

    # ---- network / QR -----------------------------------------------------
    def refresh_networks(self, keep_ip=None):
        self.networks = candidate_ips() or [("127.0.0.1", "")]
        labels = [f"{ip}  {name}".strip() for ip, name in self.networks]
        self.net_box["values"] = labels
        ips = [ip for ip, _ in self.networks]
        index = ips.index(keep_ip) if keep_ip in ips else 0
        self.net_box.current(index)
        self.select_network(save=False)

    def select_network(self, save=True):
        self.current_ip = self.networks[self.net_box.current()][0]
        url = f"http://{self.current_ip}:{self.port}/?t={self.token}"
        self.url_var.set(url)
        img = qrcode.make(url, box_size=7, border=2).get_image().convert("RGB")
        self._qr = ImageTk.PhotoImage(img.resize((260, 260), Image.NEAREST))
        self.qr_label.configure(image=self._qr)
        if save:
            save_settings(ip=self.current_ip)

    def copy_url(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.url_var.get())
        self.copy_btn.configure(text=self.t("copied"))
        self.root.after(1500, lambda: self.copy_btn.configure(text=self.t("copy")))

    # ---- state ------------------------------------------------------------
    def show_server_state(self):
        if self.server.error is not None:
            self.status.configure(text=self.t("port_busy", port=self.port), style="Err.TLabel", wraplength=420)
        else:
            self.status.configure(text="● " + self.t("app_running", port=self.port), style="Ok.TLabel")

    def _refresh_clients(self):
        items = self.clients.snapshot()
        key = [c["id"] for c in items]
        if key == self._shown_clients:
            return
        self._shown_clients = key
        self.tree.delete(*self.tree.get_children())
        for c in items:
            since = time.strftime("%H:%M", time.localtime(c["since"]))
            self.tree.insert("", "end", values=(c["address"], describe_device(c["user_agent"]), since))
        if items:
            self.empty_label.pack_forget()
        else:
            self.empty_label.pack(anchor="e" if self.lang in RTL else "w", pady=(2, 10), after=self.tree)
        if self.tray is not None:
            self.tray.title = f"PocketTap · {len(items)}"

    def _append_log(self, line):
        self.log_view.configure(state="normal")
        self.log_view.insert("end", line + "\n")
        # Keep the view light on long runs.
        if int(self.log_view.index("end-1c").split(".")[0]) > 1000:
            self.log_view.delete("1.0", "200.0")
        self.log_view.configure(state="disabled")
        self.log_view.see("end")

    def _poll(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == "log":
                    self._append_log(payload)
                elif kind == "call":
                    payload()
        except queue.Empty:
            pass
        self._refresh_clients()
        self.root.after(POLL_MS, self._poll)

    def call_soon(self, fn):
        """Run fn on the window's thread (from the tray or worker threads)."""
        self.events.put(("call", fn))

    # ---- updates ----------------------------------------------------------
    def check_updates(self, quiet=False):
        def work():
            try:
                found = check_for_update(__version__)
            except Exception as exc:  # noqa: BLE001 - offline is normal, just report it
                if not quiet:
                    log.warning(self.t("update_failed", error=exc))
                return
            if found:
                self.call_soon(lambda: self.show_update(*found))
            elif not quiet:
                log.info(self.t("up_to_date", version=__version__))
        threading.Thread(target=work, name="pockettap-update", daemon=True).start()

    def _periodic_update_check(self):
        self.check_updates(quiet=True)
        self.root.after(UPDATE_EVERY_MS, self._periodic_update_check)

    def show_update(self, tag, url):
        self.update_url = url
        text = self.t("update_available", version=tag)
        self.update_label.configure(text=text)
        self.update_bar.pack(fill="x", pady=(10, 0), before=self.body)
        log.info(text)
        if self.tray is not None:
            try:
                self.tray.notify(text, "PocketTap")
            except Exception:  # noqa: BLE001 - notifications are optional
                pass

    def open_update(self):
        if self.update_url:
            webbrowser.open(self.update_url)

    # ---- window / tray ----------------------------------------------------
    def _start_tray(self):
        # pystray's detached mode shares the process with Tk reliably on Windows only;
        # elsewhere closing the window minimizes it and the server keeps running.
        if sys.platform != "win32":
            return
        try:
            import pystray
        except Exception as exc:  # noqa: BLE001 - no tray support: closing minimizes instead
            log.info("tray unavailable: %s", exc)
            return
        menu = pystray.Menu(
            pystray.MenuItem(self.t("tray_open"), lambda: self.call_soon(self.show), default=True),
            pystray.MenuItem(self.t("tray_check"), lambda: self.call_soon(self.check_updates)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(self.t("tray_quit"), lambda: self.call_soon(self.quit)),
        )
        try:
            self.tray = pystray.Icon("PocketTap", tray_image(64), "PocketTap", menu)
            self.tray.run_detached()
        except Exception as exc:  # noqa: BLE001
            log.info("tray unavailable: %s", exc)
            self.tray = None

    def hide(self):
        if self.tray is None:
            self.root.iconify()
            return
        self.root.withdraw()
        if not self.tray_hint_shown:
            self.tray_hint_shown = True
            try:
                self.tray.notify(self.t("tray_hidden"), "PocketTap")
            except Exception:  # noqa: BLE001
                pass

    def show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def quit(self):
        if self.tray is not None:
            self.tray.stop()
        self.server.stop()
        self.root.destroy()

    def run(self, start_hidden=False):
        if start_hidden:
            self.root.withdraw() if self.tray is not None else self.root.iconify()
        self.root.mainloop()
