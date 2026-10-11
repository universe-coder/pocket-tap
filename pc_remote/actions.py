"""Named remote actions and the key combos they press on the PC.

A combo is a tuple of key names pressed together, e.g. ("shift", "n").
Key names are either a single character or one of SPECIAL_KEYS.
"""

SPECIAL_KEYS = frozenset({
    "space", "enter", "esc", "backspace", "tab", "delete", "home", "end",
    "page_up", "page_down", "left", "right", "up", "down",
    "shift", "ctrl", "alt", "cmd",
    "f5", "f11",
    "media_play_pause", "media_next", "media_previous",
    "media_volume_up", "media_volume_down", "media_volume_mute",
})

# Play/pause, next and previous are media keys: Windows, macOS and Linux route
# them to whatever is playing (browser tab, Spotify, VLC, ...) even when that
# window is not focused. Seek and full screen use the keys most players share
# (arrows, F) and need the player window in focus. Speed and captions are
# YouTube hotkeys; the page labels them as such.
ACTIONS = {
    # Any player
    "media.play_pause": ("media_play_pause",),
    "media.next": ("media_next",),
    "media.previous": ("media_previous",),
    "media.seek_back": ("left",),
    "media.seek_fwd": ("right",),
    "media.fullscreen": ("f",),
    # YouTube only
    "yt.captions": ("c",),
    "yt.speed_up": ("shift", "."),
    "yt.speed_down": ("shift", ","),
    # System
    "sys.volume_up": ("media_volume_up",),
    "sys.volume_down": ("media_volume_down",),
    "sys.volume_mute": ("media_volume_mute",),
    # Browser
    "browser.back": ("alt", "left"),
    "browser.forward": ("alt", "right"),
    "browser.refresh": ("f5",),
    "browser.fullscreen": ("f11",),
}

MOUSE_BUTTONS = frozenset({"left", "right", "middle"})


def is_valid_key(name: str) -> bool:
    return name in SPECIAL_KEYS or (len(name) == 1 and name.isprintable())
