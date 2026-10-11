"""Check GitHub for a newer release of the PC program."""

import json
import re
import urllib.request

REPO = "universe-coder/pocket-tap"
RELEASES_URL = f"https://github.com/{REPO}/releases/latest"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"


def parse_version(text):
    """'v1.2.0' -> (1, 2, 0); None if it is not a plain version."""
    m = re.fullmatch(r"v?(\d+(?:\.\d+)*)", text.strip())
    return tuple(int(p) for p in m.group(1).split(".")) if m else None


def is_newer(candidate, current):
    a, b = parse_version(candidate), parse_version(current)
    if a is None or b is None:
        return False
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


def latest_release(timeout=10):
    """(tag, page URL) of the latest published release. Raises OSError/ValueError on failure."""
    req = urllib.request.Request(API_URL, headers={"Accept": "application/vnd.github+json",
                                                   "User-Agent": "PocketTap update check"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.load(resp)
    return data["tag_name"], data.get("html_url") or RELEASES_URL


def check_for_update(current, timeout=10):
    """(tag, URL) if a newer release exists, else None. Raises on network errors."""
    tag, url = latest_release(timeout)
    return (tag, url) if is_newer(tag, current) else None
