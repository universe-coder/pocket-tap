"""Entry point: `python -m pc_remote`."""

import argparse
import asyncio
import logging
import os
import secrets
import sys
from pathlib import Path

from aiohttp import web

from . import __version__
from .app import create_app
from .i18n import LANGUAGES, detect_language, tr
from .net import candidate_ips

DEFAULT_PORT = 8765


def config_dir():
    base = os.environ.get("APPDATA") if sys.platform == "win32" else None
    return Path(base) / "pc-remote" if base else Path.home() / ".pc-remote"


def load_token(reset=False):
    """Keep one token across restarts so the phone does not need re-pairing."""
    path = config_dir() / "token"
    if path.exists() and not reset:
        token = path.read_text().strip()
        if token:
            return token
    token = secrets.token_urlsafe(16)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token)
    return token


def make_loop():
    """Event loop for the server.

    Windows defaults to the Proactor loop, which closes the listening socket
    for good when an accept fails (e.g. WinError 64 when the phone's VPN
    switches on mid-connection), so the server silently stops taking
    connections. The selector loop logs such an error and keeps listening.
    """
    return asyncio.SelectorEventLoop()


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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pockettap", description="PocketTap: phone remote control for this PC")
    parser.add_argument("--host", default="0.0.0.0", help="address to listen on (default: all)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--ip", help="PC address to put in the QR code (if the guessed one does not work)")
    parser.add_argument("--reset-token", action="store_true", help="issue a new pairing token")
    parser.add_argument("--lang", choices=LANGUAGES, help="language of these console messages (default: system)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--dry-run", action="store_true", help="log commands instead of pressing keys")
    args = parser.parse_args(argv)

    # Never crash on a console that cannot show some script (e.g. Arabic on cp437).
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")

    if args.dry_run:
        from .backend import DryRunBackend
        backend = DryRunBackend()
    else:
        from .backend import PynputBackend
        backend = PynputBackend()

    token = load_token(reset=args.reset_token)
    candidates = candidate_ips()
    ip = args.ip or (candidates[0][0] if candidates else "127.0.0.1")
    url = f"http://{ip}:{args.port}/?t={token}"
    lang = detect_language(args.lang)
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


if __name__ == "__main__":
    main()
