"""Run the server on a background thread, so a window can own the main thread."""

import asyncio
import logging
import threading

from aiohttp import web

log = logging.getLogger(__name__)


def make_loop():
    """Event loop for the server.

    Windows defaults to the Proactor loop, which closes the listening socket
    for good when an accept fails (e.g. WinError 64 when the phone's VPN
    switches on mid-connection), so the server silently stops taking
    connections. The selector loop logs such an error and keeps listening.
    """
    return asyncio.SelectorEventLoop()


class ServerThread(threading.Thread):
    """Serves `app` until stop(). After start(), wait on `ready`; `error` is set if
    the port could not be opened (usually another copy is already running)."""

    def __init__(self, app, host, port):
        super().__init__(name="pockettap-server", daemon=True)
        self.app, self.host, self.port = app, host, port
        self.ready = threading.Event()
        self.error = None
        self._loop = None

    def run(self):
        loop = self._loop = make_loop()
        asyncio.set_event_loop(loop)
        runner = web.AppRunner(self.app)
        loop.run_until_complete(runner.setup())
        try:
            loop.run_until_complete(web.TCPSite(runner, self.host, self.port).start())
        except OSError as exc:
            self.error = exc
            log.error("cannot listen on port %s: %s", self.port, exc)
        self.ready.set()
        if self.error is None:
            loop.run_forever()
        loop.run_until_complete(runner.cleanup())
        loop.close()

    def stop(self):
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
