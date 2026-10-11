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
from tkinter import font as tkfont
import webbrowser
from tkinter import ttk

import qrcode
from PIL import Image, ImageTk

from . import __version__
from .app import STATIC_DIR, describe_device
from .config import load_settings, save_settings
from .i18n import tr
from .net import candidate_ips
from .updates import check_for_update

log = logging.getLogger(__name__)

POLL_MS = 200

# Same palette as the phone app (static/style.css).
BG = "#0f1115"
SURFACE = "#1b1f27"
SURFACE_2 = "#232833"
BORDER = "#2a303b"
TEXT = "#f2f4f8"
MUTED = "#9aa3b2"
ACCENT = "#ff3b3b"
ACCENT_PRESSED = "#d92f2f"
OK = "#3ccf7a"
ERROR = "#ff6b6b"
WARN_BG = "#2b2414"
WARN_BORDER = "#5c4a1c"
WARN_TEXT = "#ffd479"
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
    """The PocketTap icon; small sizes use a simpler drawing that stays readable."""
    name = "icon-small.png" if size <= 40 else "icon-512.png"
    with Image.open(STATIC_DIR / name) as img:
        return img.convert("RGBA").resize((size, size), Image.LANCZOS)


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
        self.root.geometry("920x700")
        self.root.minsize(840, 660)
        try:
            self._icons = [ImageTk.PhotoImage(tray_image(n)) for n in (64, 32, 16)]
            self.root.iconphoto(True, *self._icons)
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
    def _fonts(self):
        families = set(tkfont.families(self.root))
        ui = next((f for f in ("Segoe UI", "SF Pro Text", "Helvetica Neue", "Noto Sans", "DejaVu Sans") if f in families), "TkDefaultFont")
        mono = next((f for f in ("Cascadia Mono", "Consolas", "Menlo", "DejaVu Sans Mono") if f in families), "TkFixedFont")
        return ui, mono

    def _style(self):
        ui, mono = self._fonts()
        self.f_body = (ui, 10)
        self.f_small = (ui, 9)
        self.f_title = (ui, 18, "bold")
        self.f_section = (ui, 11, "bold")
        self.f_mono = (mono, 9)
        root = self.root
        root.configure(bg=BG)
        root.option_add("*TCombobox*Listbox.background", SURFACE_2)
        root.option_add("*TCombobox*Listbox.foreground", TEXT)
        root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        root.option_add("*TCombobox*Listbox.selectForeground", "white")
        root.option_add("*TCombobox*Listbox.font", self.f_body)

        st = ttk.Style(root)
        st.theme_use("clam")
        st.configure(".", background=BG, foreground=TEXT, font=self.f_body, borderwidth=0,
                     focuscolor=ACCENT, troughcolor=SURFACE, bordercolor=BORDER,
                     lightcolor=BORDER, darkcolor=BORDER)
        for name, bg, active in (("Accent", ACCENT, ACCENT_PRESSED), ("Ghost", SURFACE_2, BORDER)):
            st.configure(f"{name}.TButton", background=bg, foreground="white" if name == "Accent" else TEXT,
                         padding=(14, 8), font=(ui, 10, "bold"), borderwidth=0, relief="flat")
            st.map(f"{name}.TButton", background=[("pressed", active), ("active", active)])
        st.configure("TCombobox", fieldbackground=SURFACE_2, background=SURFACE_2, foreground=TEXT,
                     arrowcolor=MUTED, padding=6, borderwidth=0)
        st.map("TCombobox", fieldbackground=[("readonly", SURFACE_2)], foreground=[("readonly", TEXT)],
               selectbackground=[("readonly", SURFACE_2)], selectforeground=[("readonly", TEXT)])
        st.configure("TEntry", fieldbackground=SURFACE_2, foreground=TEXT, padding=6, borderwidth=0)
        st.map("TEntry", fieldbackground=[("readonly", SURFACE_2)])
        st.configure("Treeview", background=SURFACE, fieldbackground=SURFACE, foreground=TEXT,
                     rowheight=30, borderwidth=0, font=self.f_body)
        st.map("Treeview", background=[("selected", SURFACE_2)], foreground=[("selected", TEXT)])
        st.configure("Treeview.Heading", background=SURFACE, foreground=MUTED, font=self.f_small,
                     borderwidth=0, relief="flat", padding=(4, 4))
        st.map("Treeview.Heading", background=[("active", SURFACE)])
        st.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        st.configure("Vertical.TScrollbar", background=SURFACE_2, troughcolor=BG, arrowcolor=MUTED,
                     bordercolor=BG, lightcolor=SURFACE_2, darkcolor=SURFACE_2, borderwidth=0, gripcount=0,
                     arrowsize=12)
        st.map("Vertical.TScrollbar", background=[("active", BORDER)])

    def _card(self, parent, **pack):
        card = tk.Frame(parent, bg=SURFACE, highlightthickness=1, highlightbackground=BORDER, padx=16, pady=14)
        card.pack(**pack)
        return card

    def _label(self, parent, text="", fg=TEXT, font=None, bg=SURFACE, **kw):
        return tk.Label(parent, text=text, fg=fg, bg=bg, font=font or self.f_body, **kw)

    def _build(self):
        self._style()
        rtl = self.lang in RTL
        anchor = "e" if rtl else "w"
        justify = "right" if rtl else "left"
        outer = tk.Frame(self.root, bg=BG, padx=20, pady=16)
        outer.pack(fill="both", expand=True)

        # Header: logo, name, version, server status pill.
        head = tk.Frame(outer, bg=BG)
        head.pack(fill="x")
        self._logo = ImageTk.PhotoImage(tray_image(40))
        tk.Label(head, image=self._logo, bg=BG).pack(side="left")
        self._label(head, "PocketTap", font=self.f_title, bg=BG).pack(side="left", padx=(10, 6))
        self._label(head, f"v{__version__}", fg=MUTED, font=self.f_small, bg=BG).pack(side="left", pady=(8, 0))
        self.status = tk.Label(head, text="", bg=SURFACE, fg=TEXT, font=self.f_small, padx=12, pady=6,
                               highlightthickness=1, highlightbackground=BORDER)
        self.status.pack(side="right")

        # Update banner, shown only when GitHub has a newer release.
        self.update_bar = tk.Frame(outer, bg=WARN_BG, padx=14, pady=10, highlightthickness=1,
                                   highlightbackground=WARN_BORDER)
        self.update_label = self._label(self.update_bar, fg=WARN_TEXT, bg=WARN_BG, font=(self.f_body[0], 10, "bold"))
        self.update_label.pack(side="left")
        ttk.Button(self.update_bar, text=self.t("download"), style="Accent.TButton",
                   command=self.open_update, cursor="hand2").pack(side="right")

        body = tk.Frame(outer, bg=BG)
        body.pack(fill="both", expand=True, pady=(16, 0))
        self.body = body

        # Left: pairing card.
        left = self._card(body, side="left", fill="y", padx=(0, 16))
        self._label(left, self.t("scan"), font=self.f_section, wraplength=280, justify=justify).pack(anchor=anchor)
        qr_frame = tk.Frame(left, bg="white", padx=10, pady=10)
        qr_frame.pack(pady=(10, 10))
        self.qr_label = tk.Label(qr_frame, bg="white", bd=0)
        self.qr_label.pack()
        self.url_var = tk.StringVar()
        ttk.Entry(left, textvariable=self.url_var, state="readonly", font=self.f_small).pack(fill="x")
        self.copy_btn = ttk.Button(left, text=self.t("copy"), style="Accent.TButton", command=self.copy_url, cursor="hand2")
        self.copy_btn.pack(fill="x", pady=(8, 16))

        self._label(left, self.t("network"), font=self.f_section).pack(anchor=anchor)
        row = tk.Frame(left, bg=SURFACE)
        row.pack(fill="x", pady=(6, 6))
        self.net_var = tk.StringVar()
        self.net_box = ttk.Combobox(row, textvariable=self.net_var, state="readonly", font=self.f_body)
        self.net_box.pack(side="left", fill="x", expand=True)
        self.net_box.bind("<<ComboboxSelected>>", lambda e: self.select_network())
        ttk.Button(row, text="⟳", width=3, style="Ghost.TButton", cursor="hand2",
                   command=lambda: self.refresh_networks(self.current_ip)).pack(side="left", padx=(8, 0))
        self._label(left, self.t("network_hint"), fg=MUTED, font=self.f_small, wraplength=280,
                    justify=justify).pack(anchor=anchor)

        # Right: connected phones and log.
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        phones = self._card(right, fill="x")
        title = tk.Frame(phones, bg=SURFACE)
        title.pack(fill="x")
        self._label(title, self.t("connections"), font=self.f_section).pack(side="right" if rtl else "left")
        self.count_badge = tk.Label(title, text="0", bg=SURFACE_2, fg=MUTED, font=self.f_small, padx=8)
        self.count_badge.pack(side="right" if rtl else "left", padx=8)
        self.phones_area = tk.Frame(phones, bg=SURFACE, height=150)
        self.phones_area.pack(fill="x", pady=(10, 0))
        self.phones_area.pack_propagate(False)
        cols = ("address", "device", "since")
        self.tree = ttk.Treeview(self.phones_area, columns=cols, show="headings", height=4, selectmode="none")
        for col, width in zip(cols, (130, 230, 90)):
            self.tree.heading(col, text=self.t(f"col_{col}").upper() if self.lang in ("en", "de", "gsw", "ru") else self.t(f"col_{col}"), anchor=anchor)
            self.tree.column(col, width=width, anchor=anchor)
        self.empty_label = self._label(self.phones_area, self.t("no_connections"), fg=MUTED)

        logs = self._card(right, fill="both", expand=True, pady=(16, 0))
        self._label(logs, self.t("log"), font=self.f_section).pack(anchor=anchor)
        log_box = tk.Frame(logs, bg=SURFACE)
        log_box.pack(fill="both", expand=True, pady=(10, 0))
        self.log_view = tk.Text(log_box, height=8, state="disabled", wrap="word", font=self.f_mono,
                                bg=BG, fg=MUTED, bd=0, highlightthickness=0, padx=10, pady=8,
                                insertbackground=TEXT, selectbackground=SURFACE_2)
        scroll = ttk.Scrollbar(log_box, orient="vertical", command=self.log_view.yview)
        self.log_view.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log_view.pack(side="left", fill="both", expand=True)
        self.log_view.tag_configure("time", foreground="#5f6878")

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
        self._qr = ImageTk.PhotoImage(img.resize((220, 220), Image.NEAREST))
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
            self.status.configure(text="●  " + self.t("port_busy", port=self.port), fg=ERROR, wraplength=420,
                                  justify="left")
        else:
            self.status.configure(text="●  " + self.t("app_running", port=self.port), fg=OK)

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
        self.count_badge.configure(text=str(len(items)), bg=OK if items else SURFACE_2,
                                   fg=BG if items else MUTED)
        if items:
            self.empty_label.place_forget()
            self.tree.pack(fill="both", expand=True)
        else:
            self.tree.pack_forget()
            self.empty_label.place(relx=0.5, rely=0.5, anchor="center")
        if self.tray is not None:
            self.tray.title = f"PocketTap · {len(items)}"

    def _append_log(self, line):
        self.log_view.configure(state="normal")
        stamp, _, text = line.partition("  ")
        self.log_view.insert("end", stamp + "  ", "time")
        self.log_view.insert("end", text + "\n")
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
        self.update_bar.pack(fill="x", pady=(14, 0), before=self.body)
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
            self.tray = pystray.Icon("PocketTap", tray_image(32), "PocketTap", menu)
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
