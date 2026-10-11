"""Files the PC program keeps between runs: the pairing token and settings."""

import json
import os
import secrets
import sys
from pathlib import Path


def config_dir():
    base = os.environ.get("APPDATA") if sys.platform == "win32" else None
    return Path(base) / "pc-remote" if base else Path.home() / ".pc-remote"


def load_token(reset=False):
    """Keep one token across restarts so the phone does not need re-pairing."""
    path = config_dir() / "token"
    if path.exists() and not reset:
        token = path.read_text().strip()
        if token:
            return token
    token = secrets.token_urlsafe(16)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(token)
    return token


def load_settings():
    try:
        data = json.loads((config_dir() / "settings.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_settings(**changes):
    settings = load_settings()
    settings.update(changes)
    path = config_dir() / "settings.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2), encoding="utf-8")
