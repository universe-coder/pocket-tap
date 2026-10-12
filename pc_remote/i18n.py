"""Messages of the PC program (console and window) in the supported languages.

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
        "app_running": "Server running on port {port}",
        "port_busy": "Port {port} is busy. PocketTap may already be running: look for its icon in the tray.",
        "network": "Network",
        "network_hint": "Pick the network your phone is on (usually Wi-Fi).",
        "refresh": "Refresh",
        "copy": "Copy link",
        "copied": "Link copied",
        "connections": "Connected phones",
        "no_connections": "No phones connected",
        "col_address": "Address",
        "col_device": "Device",
        "col_since": "Since",
        "log": "Log",
        "update_available": "PocketTap {version} is available",
        "download": "Download",
        "up_to_date": "PocketTap is up to date ({version})",
        "update_failed": "Could not check for updates: {error}",
        "tray_open": "Open PocketTap",
        "tray_check": "Check for updates",
        "tray_quit": "Quit",
        "tray_hidden": "PocketTap keeps running in the tray. Right-click the icon to quit.",
        "mac_accessibility": "macOS has not allowed PocketTap to control the keyboard and mouse yet. Turn it on in System Settings → Privacy & Security → Accessibility (for PocketTap, or for your terminal if you started it from one), then restart PocketTap.",
    },
    "ar": {
        "scan": "امسح رمز QR بهاتفك (على شبكة Wi-Fi نفسها مع هذا الكمبيوتر)",
        "other_ips": "لا تفتح الصفحة؟ جرّب عنوانًا آخر للكمبيوتر، مثلًا: {cmd} --ip ADDRESS",
        "app_running": "الخادم يعمل على المنفذ {port}",
        "port_busy": "المنفذ {port} مشغول. ربما يعمل PocketTap بالفعل: ابحث عن أيقونته في علبة النظام.",
        "network": "الشبكة",
        "network_hint": "اختر الشبكة التي يتصل بها هاتفك (عادةً Wi-Fi).",
        "refresh": "تحديث",
        "copy": "نسخ الرابط",
        "copied": "تم نسخ الرابط",
        "connections": "الهواتف المتصلة",
        "no_connections": "لا توجد هواتف متصلة",
        "col_address": "العنوان",
        "col_device": "الجهاز",
        "col_since": "منذ",
        "log": "السجل",
        "update_available": "يتوفر PocketTap {version}",
        "download": "تنزيل",
        "up_to_date": "PocketTap محدَّث ({version})",
        "update_failed": "تعذّر التحقق من التحديثات: {error}",
        "tray_open": "فتح PocketTap",
        "tray_check": "التحقق من التحديثات",
        "tray_quit": "إنهاء",
        "tray_hidden": "يستمر PocketTap في العمل في علبة النظام. انقر على الأيقونة بزر الماوس الأيمن للإنهاء.",
        "mac_accessibility": "لم يسمح macOS بعد لـ PocketTap بالتحكم في لوحة المفاتيح والماوس. فعّل ذلك في إعدادات النظام ← الخصوصية والأمان ← تسهيلات الاستخدام (لـ PocketTap، أو للطرفية إذا شغّلته منها)، ثم أعد تشغيل PocketTap.",
    },
    "zh": {
        "scan": "用手机扫描二维码（手机和电脑需连接同一 Wi-Fi）",
        "other_ips": "打不开？试试电脑的其他地址，例如：{cmd} --ip 地址",
        "app_running": "服务器正在端口 {port} 上运行",
        "port_busy": "端口 {port} 已被占用。PocketTap 可能已在运行：请在托盘中查找它的图标。",
        "network": "网络",
        "network_hint": "选择手机所在的网络（通常是 Wi-Fi）。",
        "refresh": "刷新",
        "copy": "复制链接",
        "copied": "链接已复制",
        "connections": "已连接的手机",
        "no_connections": "没有已连接的手机",
        "col_address": "地址",
        "col_device": "设备",
        "col_since": "连接时间",
        "log": "日志",
        "update_available": "PocketTap {version} 已发布",
        "download": "下载",
        "up_to_date": "PocketTap 已是最新版本（{version}）",
        "update_failed": "无法检查更新：{error}",
        "tray_open": "打开 PocketTap",
        "tray_check": "检查更新",
        "tray_quit": "退出",
        "tray_hidden": "PocketTap 会继续在托盘中运行。右键单击图标即可退出。",
        "mac_accessibility": "macOS 尚未允许 PocketTap 控制键盘和鼠标。请在“系统设置 → 隐私与安全性 → 辅助功能”中为 PocketTap（如果从终端启动，则为终端）开启权限，然后重新启动 PocketTap。",
    },
    "ja": {
        "scan": "スマートフォンでQRコードを読み取ってください（このPCと同じWi-Fiに接続）",
        "other_ips": "開かない場合は、PCの別のアドレスを試してください。例：{cmd} --ip アドレス",
        "app_running": "サーバーはポート {port} で動作中",
        "port_busy": "ポート {port} は使用中です。PocketTap がすでに起動している可能性があります。トレイのアイコンを確認してください。",
        "network": "ネットワーク",
        "network_hint": "スマートフォンがつながっているネットワーク（通常は Wi-Fi）を選んでください。",
        "refresh": "更新",
        "copy": "リンクをコピー",
        "copied": "リンクをコピーしました",
        "connections": "接続中のスマートフォン",
        "no_connections": "接続中のスマートフォンはありません",
        "col_address": "アドレス",
        "col_device": "デバイス",
        "col_since": "接続時刻",
        "log": "ログ",
        "update_available": "PocketTap {version} が利用できます",
        "download": "ダウンロード",
        "up_to_date": "PocketTap は最新です（{version}）",
        "update_failed": "更新を確認できませんでした: {error}",
        "tray_open": "PocketTap を開く",
        "tray_check": "更新を確認",
        "tray_quit": "終了",
        "tray_hidden": "PocketTap はトレイで動作し続けます。終了するにはアイコンを右クリックしてください。",
        "mac_accessibility": "macOS がまだ PocketTap にキーボードとマウスの操作を許可していません。「システム設定 → プライバシーとセキュリティ → アクセシビリティ」で PocketTap（ターミナルから起動した場合はターミナル）をオンにして、PocketTap を再起動してください。",
    },
    "ru": {
        "scan": "Отсканируйте QR-код телефоном (телефон и ПК в одной Wi-Fi сети)",
        "other_ips": "Не открывается? Попробуйте другой адрес ПК, например: {cmd} --ip АДРЕС",
        "app_running": "Сервер работает на порту {port}",
        "port_busy": "Порт {port} занят. Возможно, PocketTap уже запущен: поищите его значок в трее.",
        "network": "Сеть",
        "network_hint": "Выберите сеть, в которой телефон (обычно Wi-Fi).",
        "refresh": "Обновить",
        "copy": "Копировать ссылку",
        "copied": "Ссылка скопирована",
        "connections": "Подключённые телефоны",
        "no_connections": "Телефоны не подключены",
        "col_address": "Адрес",
        "col_device": "Устройство",
        "col_since": "Подключён",
        "log": "Журнал",
        "update_available": "Доступна версия PocketTap {version}",
        "download": "Скачать",
        "up_to_date": "У вас последняя версия PocketTap ({version})",
        "update_failed": "Не удалось проверить обновления: {error}",
        "tray_open": "Открыть PocketTap",
        "tray_check": "Проверить обновления",
        "tray_quit": "Выход",
        "tray_hidden": "PocketTap продолжает работать в трее. Чтобы выйти, щёлкните значок правой кнопкой.",
        "mac_accessibility": "macOS ещё не разрешила PocketTap управлять клавиатурой и мышью. Включите это в Системных настройках → Конфиденциальность и безопасность → Универсальный доступ (для PocketTap или для терминала, если запускали из него) и перезапустите PocketTap.",
    },
    "de": {
        "scan": "Scanne den QR-Code mit dem Handy (im selben WLAN wie dieser PC)",
        "other_ips": "Lädt nicht? Probiere eine andere PC-Adresse, z. B.: {cmd} --ip ADRESSE",
        "app_running": "Server läuft auf Port {port}",
        "port_busy": "Port {port} ist belegt. PocketTap läuft vielleicht schon: Suche das Symbol im Infobereich.",
        "network": "Netzwerk",
        "network_hint": "Wähle das Netzwerk, in dem dein Handy ist (meist WLAN).",
        "refresh": "Aktualisieren",
        "copy": "Link kopieren",
        "copied": "Link kopiert",
        "connections": "Verbundene Handys",
        "no_connections": "Keine Handys verbunden",
        "col_address": "Adresse",
        "col_device": "Gerät",
        "col_since": "Seit",
        "log": "Protokoll",
        "update_available": "PocketTap {version} ist verfügbar",
        "download": "Herunterladen",
        "up_to_date": "PocketTap ist aktuell ({version})",
        "update_failed": "Updates konnten nicht geprüft werden: {error}",
        "tray_open": "PocketTap öffnen",
        "tray_check": "Nach Updates suchen",
        "tray_quit": "Beenden",
        "tray_hidden": "PocketTap läuft im Infobereich weiter. Zum Beenden mit der rechten Maustaste auf das Symbol klicken.",
        "mac_accessibility": "macOS hat PocketTap noch nicht erlaubt, Tastatur und Maus zu steuern. Schalten Sie es unter Systemeinstellungen → Datenschutz & Sicherheit → Bedienungshilfen ein (für PocketTap oder für das Terminal, falls Sie es von dort gestartet haben) und starten Sie PocketTap neu.",
    },
    "gsw": {
        "scan": "Scann de QR-Code mit em Handy (im gliiche WLAN wie dä PC)",
        "other_ips": "Lädt nöd? Probier en anderi PC-Adrässe, z. B.: {cmd} --ip ADRÄSSE",
        "app_running": "Server lauft uf Port {port}",
        "port_busy": "Port {port} isch bsetzt. PocketTap lauft villicht scho: Lueg nach em Symbol im Infobereich.",
        "network": "Netzwerk",
        "network_hint": "Wähl s Netzwerk, wo dis Handy drin isch (meistens WLAN).",
        "refresh": "Aktualisiere",
        "copy": "Link kopiere",
        "copied": "Link kopiert",
        "connections": "Verbundeni Handys",
        "no_connections": "Kei Handys verbunde",
        "col_address": "Adrässe",
        "col_device": "Grät",
        "col_since": "Sit",
        "log": "Protokoll",
        "update_available": "PocketTap {version} isch verfüegbar",
        "download": "Abelade",
        "up_to_date": "PocketTap isch aktuell ({version})",
        "update_failed": "Updates händ nöd chöne prüeft werde: {error}",
        "tray_open": "PocketTap öffne",
        "tray_check": "Nach Updates sueche",
        "tray_quit": "Beände",
        "tray_hidden": "PocketTap lauft im Infobereich wiiter. Zum Beände mit de rächte Muustaste ufs Symbol klicke.",
        "mac_accessibility": "macOS het PocketTap no nöd erlaubt, Tastatur und Muus z stüüre. Schalt das under Systemiistellige → Dateschutz & Sicherheit → Bedienigshilfe ii (für PocketTap oder fürs Terminal, wenn du s vo dört gstartet hesch) und start PocketTap neu.",
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
