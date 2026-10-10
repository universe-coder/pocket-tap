import os
import sys

# Headless Linux CI has no X server; pynput's dummy backend still exposes the
# Key enum, which is all the key-name test needs.
if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
    os.environ.setdefault("PYNPUT_BACKEND", "dummy")
