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

# Play/pause, next and previous use media keys: Chrome, Edge and Firefox route
# them to the YouTube tab even when the browser window is not focused.
# The rest are YouTube player hotkeys and need the YouTube tab in focus.
ACTIONS = {
    # YouTube
    "yt.play_pause": ("media_play_pause",),
    "yt.next": ("media_next",),
    "yt.previous": ("media_previous",),
    "yt.seek_back_10": ("j",),
    "yt.seek_fwd_10": ("l",),
    "yt.seek_back_5": ("left",),
    "yt.seek_fwd_5": ("right",),
    "yt.fullscreen": ("f",),
    "yt.theater": ("t",),
    "yt.mute": ("m",),
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
