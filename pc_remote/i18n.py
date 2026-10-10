"""Console messages of the PC program in the supported languages.

The phone app has its own translations in static/locales/*.json.
"""

import locale
import os
import sys

LANGUAGES = ("en", "ar", "zh", "ja", "ru", "de", "gsw")

MESSAGES = {
    "en": {
        "scan": "Scan the QR code with your phone (same Wi-Fi as this PC)",
        "other_ips": "Not loading? Try another PC address, e.g.: {cmd} --ip ADDRESS",
    },
    "ar": {
        "scan": "امسح رمز QR بهاتفك (على شبكة Wi-Fi نفسها مع هذا الكمبيوتر)",
        "other_ips": "لا تفتح الصفحة؟ جرّب عنوانًا آخر للكمبيوتر، مثلًا: {cmd} --ip ADDRESS",
    },
    "zh": {
        "scan": "用手机扫描二维码（手机和电脑需连接同一 Wi-Fi）",
        "other_ips": "打不开？试试电脑的其他地址，例如：{cmd} --ip 地址",
    },
    "ja": {
        "scan": "スマートフォンでQRコードを読み取ってください（このPCと同じWi-Fiに接続）",
        "other_ips": "開かない場合は、PCの別のアドレスを試してください。例：{cmd} --ip アドレス",
    },
    "ru": {
        "scan": "Отсканируйте QR-код телефоном (телефон и ПК в одной Wi-Fi сети)",
        "other_ips": "Не открывается? Попробуйте другой адрес ПК, например: {cmd} --ip АДРЕС",
    },
    "de": {
        "scan": "Scanne den QR-Code mit dem Handy (im selben WLAN wie dieser PC)",
        "other_ips": "Lädt nicht? Probiere eine andere PC-Adresse, z. B.: {cmd} --ip ADRESSE",
    },
    "gsw": {
        "scan": "Scann de QR-Code mit em Handy (im gliiche WLAN wie dä PC)",
        "other_ips": "Lädt nöd? Probier en anderi PC-Adrässe, z. B.: {cmd} --ip ADRÄSSE",
    },
}


def normalize(tag):
    """Map a locale name like 'de_CH.UTF-8' or 'zh-Hans' to a supported code, or None."""
    if not tag:
        return None
    code = tag.replace("_", "-").split(".")[0].lower()
    if code.startswith("gsw") or code == "de-ch":
        return "gsw"
    base = code.split("-")[0]
    return base if base in LANGUAGES else None


def _system_locale():
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        if os.environ.get(var):
            return os.environ[var]
    if sys.platform == "win32":
        try:
            import ctypes
            lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return locale.windows_locale.get(lcid)
        except (AttributeError, OSError):
            pass
    try:
        return locale.getlocale()[0]
    except ValueError:
        return None


def detect_language(preferred=None):
    return normalize(preferred) or normalize(_system_locale()) or "en"


def tr(lang, key, **kwargs):
    return MESSAGES.get(lang, MESSAGES["en"])[key].format(**kwargs)
