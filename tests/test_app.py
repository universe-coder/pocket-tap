import pytest

from pc_remote.actions import ACTIONS, SPECIAL_KEYS, is_valid_key
from pc_remote.app import BadMessage, create_app, handle_message
from pc_remote.backend import DryRunBackend

TOKEN = "secret-token"


@pytest.fixture
def backend():
    return DryRunBackend()


@pytest.fixture
async def client(aiohttp_client, backend):
    return await aiohttp_client(create_app(backend, TOKEN))


def test_every_action_uses_known_keys():
    for name, combo in ACTIONS.items():
        assert combo, name
        assert all(is_valid_key(k) for k in combo), name


def test_special_keys_resolve_in_pynput():
    pynput_key = pytest.importorskip("pynput.keyboard", exc_type=ImportError).Key
    for name in SPECIAL_KEYS:
        assert hasattr(pynput_key, name), name


@pytest.mark.parametrize("msg, call", [
    ({"type": "action", "name": "yt.play_pause"}, ("combo", ("media_play_pause",))),
    ({"type": "action", "name": "yt.speed_up"}, ("combo", ("shift", "."))),
    ({"type": "key", "keys": ["ctrl", "w"]}, ("combo", ("ctrl", "w"))),
    ({"type": "text", "text": "привет"}, ("text", "привет")),
    ({"type": "move", "dx": 5, "dy": -3.7}, ("move", 5, -3)),
    ({"type": "move", "dx": 10**9, "dy": 0}, ("move", 2000, 0)),
    ({"type": "click", "button": "right"}, ("click", "right", 1)),
    ({"type": "click", "double": True}, ("click", "left", 2)),
    ({"type": "scroll", "dy": -2}, ("scroll", 0, -2)),
])
def test_handle_message(backend, msg, call):
    handle_message(backend, msg)
    assert backend.calls == [call]


@pytest.mark.parametrize("msg", [
    [],
    {"type": "nope"},
    {"type": "action", "name": "rm -rf"},
    {"type": "key", "keys": ["ctrl", "notakey"]},
    {"type": "key", "keys": []},
    {"type": "key", "keys": "enter"},
    {"type": "text", "text": ""},
    {"type": "text", "text": "x" * 501},
    {"type": "move", "dx": "1"},
    {"type": "move", "dx": True},
    {"type": "click", "button": "x1"},
])
def test_handle_message_rejects(backend, msg):
    with pytest.raises(BadMessage):
        handle_message(backend, msg)
    assert backend.calls == []


async def test_index_and_static_served(client):
    resp = await client.get("/")
    assert resp.status == 200
    assert "PC Remote" in await resp.text()
    for path in ("/static/app.js", "/static/style.css", "/static/manifest.webmanifest", "/static/icon.svg"):
        assert (await client.get(path)).status == 200, path


async def test_check_endpoint(client):
    assert (await client.get(f"/check?t={TOKEN}")).status == 204
    assert (await client.get("/check?t=wrong")).status == 401


async def test_websocket_rejects_bad_token(client):
    resp = await client.get("/ws?t=wrong")
    assert resp.status == 401


async def test_websocket_drives_backend(client, backend):
    async with client.ws_connect(f"/ws?t={TOKEN}") as ws:
        assert (await ws.receive_json())["type"] == "hello"
        await ws.send_json({"type": "action", "name": "yt.seek_fwd_10"})
        await ws.send_json({"type": "action", "name": "bogus"})
        error = await ws.receive_json()
        assert error["type"] == "error"
        await ws.send_str("not json")
        assert (await ws.receive_json())["type"] == "error"
    assert backend.calls == [("combo", ("l",))]
