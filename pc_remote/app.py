"""HTTP + WebSocket server: serves the phone UI and turns its messages into input."""

import hmac
import itertools
import json
import re
import logging
import threading
import time
from pathlib import Path

from aiohttp import WSMsgType, web

from .actions import ACTIONS, MOUSE_BUTTONS, is_valid_key

log = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).parent / "static"
MAX_TEXT_LEN = 500
MAX_MOVE = 2000
MAX_SCROLL = 50

BACKEND_KEY = web.AppKey("backend", object)
TOKEN_KEY = web.AppKey("token", str)


class Clients:
    """Phones connected right now. Read from other threads (the PC window)."""

    def __init__(self):
        self._lock = threading.Lock()
        self._items = {}
        self._ids = itertools.count(1)

    def add(self, address, user_agent):
        with self._lock:
            cid = next(self._ids)
            self._items[cid] = {"address": address, "user_agent": user_agent, "since": time.time()}
            return cid

    def remove(self, cid):
        with self._lock:
            self._items.pop(cid, None)

    def snapshot(self):
        with self._lock:
            return [dict(c, id=cid) for cid, c in self._items.items()]


CLIENTS_KEY = web.AppKey("clients", Clients)


class BadMessage(ValueError):
    pass


def _int(msg, field, limit):
    value = msg.get(field, 0)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BadMessage(f"{field} must be a number")
    return max(-limit, min(limit, int(value)))


def handle_message(backend, msg):
    """Validate one decoded client message and apply it to the backend."""
    if not isinstance(msg, dict):
        raise BadMessage("message must be an object")
    kind = msg.get("type")

    if kind == "action":
        combo = ACTIONS.get(msg.get("name"))
        if combo is None:
            raise BadMessage(f"unknown action {msg.get('name')!r}")
        backend.press_combo(combo)
    elif kind == "key":
        keys = msg.get("keys")
        if (not isinstance(keys, list) or not 1 <= len(keys) <= 4
                or not all(isinstance(k, str) and is_valid_key(k) for k in keys)):
            raise BadMessage("keys must be a list of 1-4 known key names")
        backend.press_combo(keys)
    elif kind == "text":
        text = msg.get("text")
        if not isinstance(text, str) or not 0 < len(text) <= MAX_TEXT_LEN:
            raise BadMessage(f"text must be 1-{MAX_TEXT_LEN} characters")
        backend.type_text(text)
    elif kind == "move":
        backend.mouse_move(_int(msg, "dx", MAX_MOVE), _int(msg, "dy", MAX_MOVE))
    elif kind == "click":
        button = msg.get("button", "left")
        if button not in MOUSE_BUTTONS:
            raise BadMessage(f"unknown mouse button {button!r}")
        count = 2 if msg.get("double") else 1
        backend.click(button, count)
    elif kind == "scroll":
        backend.scroll(_int(msg, "dx", MAX_SCROLL), _int(msg, "dy", MAX_SCROLL))
    elif kind == "ping":
        pass
    else:
        raise BadMessage(f"unknown message type {kind!r}")


def _authorized(request):
    given = request.query.get("t", "")
    return hmac.compare_digest(given.encode(), request.app[TOKEN_KEY].encode())


async def check_handler(request):
    if not _authorized(request):
        raise web.HTTPUnauthorized(text="bad token")
    return web.Response(status=204)


async def ws_handler(request):
    if not _authorized(request):
        log.warning("rejected connection from %s: bad token", request.remote)
        raise web.HTTPUnauthorized(text="bad token")

    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    log.info("phone connected: %s", request.remote)
    cid = request.app[CLIENTS_KEY].add(request.remote, request.headers.get("User-Agent", ""))
    try:
        await ws.send_json({"type": "hello"})
        await _serve(request.app[BACKEND_KEY], ws)
    finally:
        request.app[CLIENTS_KEY].remove(cid)
    log.info("phone disconnected: %s", request.remote)
    return ws


async def _serve(backend, ws):
    async for raw in ws:
        if raw.type != WSMsgType.TEXT:
            continue
        try:
            handle_message(backend, json.loads(raw.data))
        except (BadMessage, json.JSONDecodeError) as exc:
            await ws.send_json({"type": "error", "message": str(exc)})
        except Exception:  # noqa: BLE001 - an OS input failure must not drop the phone
            log.exception("input backend failed")
            await ws.send_json({"type": "error", "message": "input failed on PC"})


async def index(request):
    return web.FileResponse(STATIC_DIR / "index.html")


async def manifest_handler(request):
    """The web app manifest. With a valid key, the home-screen icon opens the
    remote already paired: iOS keeps a home-screen app's storage apart from
    Safari's, so the key saved in the browser is not there."""
    manifest = json.loads((STATIC_DIR / "manifest.webmanifest").read_text(encoding="utf-8"))
    if _authorized(request):
        manifest["start_url"] = "/?t=" + request.query["t"]
    return web.json_response(manifest, content_type="application/manifest+json",
                             headers={"Cache-Control": "no-store"})


def create_app(backend, token, clients=None):
    app = web.Application()
    app[CLIENTS_KEY] = clients if clients is not None else Clients()
    app[BACKEND_KEY] = backend
    app[TOKEN_KEY] = token
    app.router.add_get("/", index)
    app.router.add_get("/manifest.webmanifest", manifest_handler)
    app.router.add_get("/check", check_handler)
    app.router.add_get("/ws", ws_handler)
    app.router.add_static("/static/", STATIC_DIR)
    return app


def describe_device(user_agent):
    """Short human name for a phone from its User-Agent, e.g. 'Android 14 · Chrome'."""
    ua = user_agent or ""
    os_name = ""
    m = re.search(r"Android (\d+(?:\.\d+)?)", ua)
    if m:
        os_name = f"Android {m.group(1)}"
    elif "iPhone" in ua or "iPad" in ua:
        m = re.search(r"OS (\d+)[_\d]*", ua)
        os_name = ("iPad" if "iPad" in ua else "iPhone") + (f" · iOS {m.group(1)}" if m else "")
    elif "Windows" in ua:
        os_name = "Windows"
    elif "Mac OS X" in ua:
        os_name = "macOS"
    elif "Linux" in ua:
        os_name = "Linux"
    browser = ""
    for token, name in (("SamsungBrowser", "Samsung Internet"), ("YaBrowser", "Yandex Browser"),
                        ("EdgA", "Edge"), ("Edg/", "Edge"), ("OPR", "Opera"), ("Firefox", "Firefox"),
                        ("FxiOS", "Firefox"), ("CriOS", "Chrome"), ("Chrome", "Chrome"), ("Safari", "Safari")):
        if token in ua:
            browser = name
            break
    return " · ".join(p for p in (os_name, browser) if p) or "?"
