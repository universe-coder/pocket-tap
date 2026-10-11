import asyncio

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
    ({"type": "action", "name": "media.play_pause"}, ("combo", ("media_play_pause",))),
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
    assert "PocketTap" in await resp.text()
    for path in ("/static/app.js", "/static/style.css", "/static/manifest.webmanifest", "/static/icon.svg",
                 "/static/i18n.js", "/static/locales/en.json", "/static/locales/ar.json"):
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
        await ws.send_json({"type": "action", "name": "media.seek_fwd"})
        await ws.send_json({"type": "action", "name": "bogus"})
        error = await ws.receive_json()
        assert error["type"] == "error"
        await ws.send_str("not json")
        assert (await ws.receive_json())["type"] == "error"
    assert backend.calls == [("combo", ("right",))]


def test_candidate_ips_prefer_home_network_over_vpn():
    from pc_remote.net import candidate_ips
    adapters = [
        ("lo", "127.0.0.1"),
        ("AmneziaVPN", "10.8.1.2"),
        ("wintun", "198.18.0.1"),
        ("Tailscale", "100.101.102.103"),
        ("Ethernet 2", "169.254.10.10"),
        ("Беспроводная сеть", "192.168.1.42"),
        ("vEthernet (WSL)", "172.25.160.1"),
    ]
    ips = [ip for ip, _ in candidate_ips(adapters)]
    assert ips[0] == "192.168.1.42"
    # Loopback and link-local are never offered; the rest stay as fallbacks.
    assert sorted(ips[1:]) == sorted(["10.8.1.2", "198.18.0.1", "100.101.102.103", "172.25.160.1"])


def test_candidate_ips_home_lan_on_10_network():
    from pc_remote.net import candidate_ips
    # Some routers hand out 10.x; a VPN on 198.18.x must still lose to it.
    adapters = [("Clash", "198.18.0.1"), ("Wi-Fi", "10.0.0.15")]
    assert candidate_ips(adapters)[0][0] == "10.0.0.15"


def test_server_loop_is_selector_based():
    # The Windows Proactor loop stops accepting after one failed accept.
    import asyncio
    from pc_remote.__main__ import make_loop
    loop = make_loop()
    try:
        assert isinstance(loop, asyncio.SelectorEventLoop)
    finally:
        loop.close()


async def test_connected_phones_are_listed(aiohttp_client, backend):
    from pc_remote.app import Clients
    clients = Clients()
    client = await aiohttp_client(create_app(backend, TOKEN, clients))
    ua = "Mozilla/5.0 (Linux; Android 14; Pixel 7) Chrome/141.0 Mobile Safari/537.36"
    async with client.ws_connect(f"/ws?t={TOKEN}", headers={"User-Agent": ua}) as ws:
        await ws.receive_json()
        [phone] = clients.snapshot()
        assert phone["user_agent"] == ua and phone["address"]
    await ws.close()
    for _ in range(50):
        if not clients.snapshot():
            break
        await asyncio.sleep(0.01)
    assert clients.snapshot() == []


@pytest.mark.parametrize("ua, name", [
    ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Mobile Safari/537.36",
     "Android 10 · Chrome"),
    ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 Version/18.1 Mobile/15E148 Safari/604.1",
     "iPhone · iOS 18 · Safari"),
    ("Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 SamsungBrowser/23.0 Chrome/115.0 Mobile Safari/537.36",
     "Android 13 · Samsung Internet"),
    ("", "?"),
])
def test_describe_device(ua, name):
    from pc_remote.app import describe_device
    assert describe_device(ua) == name


@pytest.mark.parametrize("candidate, current, newer", [
    ("v1.2.0", "1.1.0", True),
    ("v1.1.0", "1.1.0", False),
    ("v1.1", "1.1.0", False),
    ("v1.10.0", "1.9.3", True),
    ("v1.0.9", "1.1.0", False),
    ("nightly", "1.1.0", False),
])
def test_is_newer(candidate, current, newer):
    from pc_remote.updates import is_newer
    assert is_newer(candidate, current) is newer


def test_server_thread_reports_busy_port(backend):
    import socket
    from pc_remote.server import ServerThread
    with socket.socket() as taken:
        taken.bind(("127.0.0.1", 0))
        taken.listen()
        port = taken.getsockname()[1]
        server = ServerThread(create_app(backend, TOKEN), "127.0.0.1", port)
        server.start()
        assert server.ready.wait(5)
        server.join(5)
    assert isinstance(server.error, OSError)


async def test_server_thread_serves_and_stops(backend):
    import socket
    import urllib.request
    from pc_remote.server import ServerThread
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = ServerThread(create_app(backend, TOKEN), "127.0.0.1", port)
    server.start()
    assert server.ready.wait(5) and server.error is None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    status = await asyncio.to_thread(lambda: opener.open(f"http://127.0.0.1:{port}/check?t={TOKEN}").status)
    assert status == 204
    server.stop()
    server.join(5)
    assert not server.is_alive()


def test_window_module_and_tray_icon():
    pytest.importorskip("tkinter")
    from pc_remote.gui import tray_image
    assert tray_image(32).size == (32, 32)
