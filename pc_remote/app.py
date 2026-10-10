"""HTTP + WebSocket server: serves the phone UI and turns its messages into input."""

import hmac
import json
import logging
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
    await ws.send_json({"type": "hello"})

    backend = request.app[BACKEND_KEY]
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

    log.info("phone disconnected: %s", request.remote)
    return ws


async def index(request):
    return web.FileResponse(STATIC_DIR / "index.html")


def create_app(backend, token):
    app = web.Application()
    app[BACKEND_KEY] = backend
    app[TOKEN_KEY] = token
    app.router.add_get("/", index)
    app.router.add_get("/check", check_handler)
    app.router.add_get("/ws", ws_handler)
    app.router.add_static("/static/", STATIC_DIR)
    return app
