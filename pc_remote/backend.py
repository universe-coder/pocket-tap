"""Input backends: the real one drives the OS through pynput, the dry-run one
only records calls (used for tests and for trying the server without side effects)."""

import logging
import sys

log = logging.getLogger(__name__)


def input_allowed(prompt=False):
    """macOS lets a program press keys and move the mouse only once the user turns
    it on under Privacy & Security > Accessibility. With prompt=True macOS shows
    its own dialog pointing there. True on other systems or when it cannot tell."""
    if sys.platform != "darwin":
        return True
    try:
        import HIServices
        options = {HIServices.kAXTrustedCheckOptionPrompt: prompt}
        return bool(HIServices.AXIsProcessTrustedWithOptions(options))
    except Exception:  # noqa: BLE001 - never block start-up on this check
        return True


class DryRunBackend:
    def __init__(self):
        self.calls = []

    def _record(self, *call):
        self.calls.append(call)
        log.info("dry-run: %s", call)

    def press_combo(self, keys):
        self._record("combo", tuple(keys))

    def type_text(self, text):
        self._record("text", text)

    def mouse_move(self, dx, dy):
        self._record("move", dx, dy)

    def click(self, button, count=1):
        self._record("click", button, count)

    def scroll(self, dx, dy):
        self._record("scroll", dx, dy)


class PynputBackend:
    def __init__(self):
        from pynput import keyboard, mouse

        self._kb = keyboard.Controller()
        self._mouse = mouse.Controller()
        self._Key = keyboard.Key
        self._Button = mouse.Button
        # macOS has no "alt+left" browser back; cmd is the usual modifier there.
        self._alt_name = "cmd" if sys.platform == "darwin" else "alt"

    def _key(self, name):
        if len(name) == 1:
            return name
        if name == "alt":
            name = self._alt_name
        return getattr(self._Key, name)

    def press_combo(self, keys):
        resolved = [self._key(k) for k in keys]
        for k in resolved:
            self._kb.press(k)
        for k in reversed(resolved):
            self._kb.release(k)

    def type_text(self, text):
        self._kb.type(text)

    def mouse_move(self, dx, dy):
        self._mouse.move(dx, dy)

    def click(self, button, count=1):
        self._mouse.click(getattr(self._Button, button), count)

    def scroll(self, dx, dy):
        self._mouse.scroll(dx, dy)
