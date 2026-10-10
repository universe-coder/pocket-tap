import json
import re

import pytest

from pc_remote.app import STATIC_DIR
from pc_remote.i18n import LANGUAGES, MESSAGES, detect_language, normalize

LOCALES = STATIC_DIR / "locales"


def load(code):
    return json.loads((LOCALES / f"{code}.json").read_text(encoding="utf-8"))


def test_phone_and_pc_offer_the_same_languages():
    assert sorted(p.stem for p in LOCALES.glob("*.json")) == sorted(LANGUAGES)
    js = (STATIC_DIR / "i18n.js").read_text(encoding="utf-8")
    picker = re.search(r"const LANGUAGES = \{(.*?)\};", js, re.S).group(1)
    assert sorted(re.findall(r"^\s*(\w+):", picker, re.M)) == sorted(LANGUAGES)


@pytest.mark.parametrize("code", LANGUAGES)
def test_locale_is_complete(code):
    strings = load(code)
    assert strings.keys() == load("en").keys()
    assert all(isinstance(v, str) and v.strip() for v in strings.values())


def test_every_key_used_by_the_page_exists():
    keys = load("en").keys()
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    js = (STATIC_DIR / "app.js").read_text(encoding="utf-8")
    used = set(re.findall(r'data-i18n(?:-aria|-placeholder)?="([^"]+)"', html))
    used |= set(re.findall(r'"((?:status|wake)\.\w+)"', js))
    assert used and used <= keys


@pytest.mark.parametrize("code", LANGUAGES)
def test_console_messages_are_complete(code):
    assert MESSAGES[code].keys() == MESSAGES["en"].keys()
    assert "{cmd}" in MESSAGES[code]["other_ips"]


@pytest.mark.parametrize("tag, code", [
    ("ru_RU.UTF-8", "ru"),
    ("de_DE", "de"),
    ("de_CH.UTF-8", "gsw"),
    ("gsw-CH", "gsw"),
    ("zh-Hans-CN", "zh"),
    ("ja_JP", "ja"),
    ("ar-EG", "ar"),
    ("fr_FR", None),
    ("C", None),
    ("", None),
])
def test_normalize(tag, code):
    assert normalize(tag) == code


def test_explicit_language_wins(monkeypatch):
    monkeypatch.setenv("LANG", "ru_RU.UTF-8")
    monkeypatch.delenv("LC_ALL", raising=False)
    monkeypatch.delenv("LC_MESSAGES", raising=False)
    assert detect_language("ja") == "ja"
    assert detect_language() == "ru"
