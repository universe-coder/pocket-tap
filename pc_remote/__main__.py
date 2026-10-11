"""Entry point: `python -m pc_remote`."""

import argparse
import logging
import logging.handlers
import os
import sys
from pathlib import Path

from aiohttp import web

from . import __version__
from .app import Clients, create_app
from .config import config_dir, load_token  # noqa: F401 - re-exported for scripts and tests
from .i18n import LANGUAGES, detect_language, tr
from .net import candidate_ips
from .server import ServerThread, make_loop  # noqa: F401 - make_loop re-exported for tests

DEFAULT_PORT = 8765


def print_qr(url):
    try:
        import qrcode
    except ImportError:
        return
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.print_ascii(invert=True)


def launch_command():
    """How the user started the program, for hints like "<cmd> --ip ADDRESS"."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).name
    return "start-windows.bat" if sys.platform == "win32" else "./start.sh"


def say(lang, key, **kwargs):
    """Print a message in the PC's language, plus English for anyone else reading."""
    print(tr(lang, key, **kwargs))
    if lang != "en":
        print(tr("en", key, **kwargs))


def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(message)s", "%H:%M:%S")
    if sys.stderr is not None:
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        root.addHandler(console)
    # The window build has no console; keep a small log file for bug reports.
    try:
        config_dir().mkdir(parents=True, exist_ok=True)
        file = logging.handlers.RotatingFileHandler(config_dir() / "pockettap.log", maxBytes=512_000,
                                                    backupCount=1, encoding="utf-8")
        file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root.addHandler(file)
    except OSError:
        pass


def run_console(args, backend, token, lang):
    candidates = candidate_ips()
    ip = args.ip or (candidates[0][0] if candidates else "127.0.0.1")
    url = f"http://{ip}:{args.port}/?t={token}"
    print()
    say(lang, "scan")
    print()
    print_qr(url)
    print(f"\n{url}\n")
    others = [(c, name) for c, name in candidates if c != ip]
    if others:
        say(lang, "other_ips", cmd=launch_command())
        for c, name in others:
            print(f"  {c}  {name}")
        print()
    web.run_app(create_app(backend, token), host=args.host, port=args.port, print=None, loop=make_loop())


def run_window(args, backend, token, lang):
    from .gui import App  # imports tkinter, Pillow and pystray only when a window is wanted

    clients = Clients()
    server = ServerThread(create_app(backend, token, clients), args.host, args.port)
    server.start()
    server.ready.wait(10)
    app = App(server, clients, token, args.port, lang, preferred_ip=args.ip)
    app.run(start_hidden=args.minimized)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pockettap", description="PocketTap: phone remote control for this PC")
    parser.add_argument("--host", default="0.0.0.0", help="address to listen on (default: all)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--ip", help="PC address to put in the QR code (if the guessed one does not work)")
    parser.add_argument("--reset-token", action="store_true", help="issue a new pairing token")
    parser.add_argument("--lang", choices=LANGUAGES, help="language of the messages (default: system)")
    parser.add_argument("--console", action="store_true", help="run in the terminal without a window")
    parser.add_argument("--minimized", action="store_true", help="start hidden in the tray")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--dry-run", action="store_true", help="log commands instead of pressing keys")
    parser.add_argument("--self-test", action="store_true", help=argparse.SUPPRESS)

    # The window build of the .exe has no console: give print() somewhere to go.
    for name in ("stdout", "stderr"):
        if getattr(sys, name) is None:
            setattr(sys, name, open(os.devnull, "w"))
    args = parser.parse_args(argv)
    if args.self_test:
        # Used by the release build: fails if the bundle misses a module the window needs.
        if sys.platform == "win32":
            import pystray  # noqa: F401
        from . import gui  # noqa: F401
        from .backend import PynputBackend  # noqa: F401
        return

    # Never crash on a console that cannot show some script (e.g. Arabic on cp437).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    setup_logging()

    if args.dry_run:
        from .backend import DryRunBackend
        backend = DryRunBackend()
    else:
        from .backend import PynputBackend
        backend = PynputBackend()

    token = load_token(reset=args.reset_token)
    lang = detect_language(args.lang)

    if not args.console:
        try:
            import tkinter  # noqa: F401
        except ImportError:
            logging.warning("no tkinter: running in the terminal")
            args.console = True
    if args.console:
        run_console(args, backend, token, lang)
    else:
        run_window(args, backend, token, lang)


if __name__ == "__main__":
    main()
