<p align="center"><img src="../pc_remote/static/icon.svg" width="128" alt="PocketTap"></p>

<h1 align="center">PocketTap</h1>

[English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · [日本語](README.ja.md) · **Русский** · [Deutsch / Schweiz](README.de.md)

Телефон становится пультом для ПК по домашнему Wi-Fi. Первый сценарий: смотреть YouTube на компьютере, стоя на беговой дорожке, и управлять видео с телефона.

[![Скачать для Windows](https://img.shields.io/badge/%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe)
[![Скачать ZIP для macOS и Linux](https://img.shields.io/badge/%D0%A1%D0%BA%D0%B0%D1%87%D0%B0%D1%82%D1%8C-macOS%20%2F%20Linux%20(.zip)-555?style=for-the-badge&logo=github)](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)

[![Release](https://img.shields.io/github/v/release/universe-coder/pocket-tap?label=release&color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/universe-coder/pocket-tap/total?color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases)
[![tests](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/github/license/universe-coder/pocket-tap?color=blue)](../LICENSE)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational)
![Phone](https://img.shields.io/badge/phone-Android%20%7C%20iPhone-informational)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Languages](https://img.shields.io/badge/languages-EN%20%7C%20AR%20%7C%20ZH%20%7C%20JA%20%7C%20RU%20%7C%20DE%20%7C%20CH-orange)
[![Stars](https://img.shields.io/github/stars/universe-coder/pocket-tap?style=social)](https://github.com/universe-coder/pocket-tap/stargazers)

## Скриншоты

<table>
<tr><td align="center"><img src="screenshots/phone-media.png" width="180" alt="Медиа"><br><sub>Медиа</sub></td><td align="center"><img src="screenshots/phone-touchpad.png" width="180" alt="Тачпад"><br><sub>Тачпад</sub></td><td align="center"><img src="screenshots/phone-keyboard.png" width="180" alt="Клавиатура"><br><sub>Клавиатура</sub></td></tr>
<tr><td align="center"><img src="screenshots/phone-arabic.png" width="180" alt="Арабский, справа налево"><br><sub>Арабский, справа налево</sub></td><td align="center"><img src="screenshots/phone-japanese.png" width="180" alt="Японский"><br><sub>Японский</sub></td><td></td></tr>
</table>

<p align="center"><img src="screenshots/pc-window.png" width="520" alt="Программа на ПК: отсканируйте QR-код телефоном"><br><sub>Программа на ПК: отсканируйте QR-код телефоном</sub></p>

Состоит из двух частей:

- **Программа для ПК** (`pc_remote`, Python). Нажимает клавиши и двигает мышь по командам с телефона. Windows основная платформа, также работает на macOS и Linux (X11).
- **Приложение для телефона**. Веб-приложение (PWA), которое ПК сам раздаёт по Wi-Fi. Ничего не нужно ставить из магазина: сканируете QR-код и при желании добавляете на главный экран, после чего оно открывается как обычное приложение. Работает на Android и iPhone.

Приложение для телефона говорит на английском, арабском (справа налево), китайском, японском, русском, немецком и швейцарском немецком. Язык берётся из настроек телефона, сменить его можно вверху экрана.

## Что умеет

**Медиа**: работает с любым плеером (YouTube, Netflix, Spotify, VLC и другими): большая кнопка пауза/воспроизведение, перемотка назад и вперёд (удерживайте для быстрой перемотки), следующее и предыдущее, громкость системы, полный экран. Для YouTube есть ещё скорость и субтитры.

**Тачпад**: курсор пальцем, касание это клик, касание двумя пальцами это правый клик, прокрутка двумя пальцами, кнопки «Назад», «Вперёд», «Обновить» для браузера.

**Клавиатура**: ввод текста на ПК (например, поиск на YouTube), Enter, Esc, стрелки и другие клавиши.

**Окно на ПК**: QR-код, выбор сети (если телефон не подключается, выберите сеть, в которой он, обычно Wi-Fi), список подключённых телефонов и журнал. Если закрыть окно, PocketTap продолжит работать в трее на Windows (на macOS и Linux окно свернётся); выйти можно через меню значка в трее. Программа сама проверяет новую версию на GitHub и предлагает её скачать.

## Запуск

### Windows: один файл, Python не нужен

1. Скачайте [PocketTap-windows.exe](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe) и запустите.
   Windows может предупредить о неизвестном издателе, потому что программа не подписана: нажмите **Подробнее**, затем **Выполнить в любом случае**.
2. Windows спросит про доступ к сети: разрешите для **частных сетей**.
3. В окне появится QR-код. Отсканируйте его камерой телефона, телефон должен быть в той же Wi-Fi сети.
4. Чтобы открывать пульт одним касанием, добавьте его на главный экран: пульт сам покажет подсказку со шагами для вашего телефона. Иконка открывает пульт уже подключённым; на iPhone он работает как обычное приложение, на Android переходит в полноэкранный режим после первого касания (по обычному Wi-Fi без HTTPS браузеры Android не дают установить его полностью).

### macOS: готовое приложение, Python не нужен

1. Скачайте [PocketTap-macos-apple-silicon.zip](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-macos-apple-silicon.zip) для Mac с чипом M1 и новее или [PocketTap-macos-intel.zip](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-macos-intel.zip) для Mac на Intel (какой у вас, видно в  → Об этом Mac). Распакуйте и перетащите PocketTap в «Программы».
2. Приложение не подписано Apple, поэтому первый запуск macOS заблокирует. Откройте PocketTap один раз, закройте предупреждение, затем в Системных настройках → Конфиденциальность и безопасность нажмите **Всё равно открыть**.
3. macOS попросит разрешить PocketTap в разделе Конфиденциальность и безопасность → **Универсальный доступ**: включите его, затем закройте и снова откройте PocketTap. Без этого программа не сможет нажимать клавиши. Если macOS спросит про входящие сетевые подключения, разрешите их.
4. Отсканируйте QR-код из окна телефоном, как на Windows.

### Любая система, с Python

1. Установите [Python 3.9+](https://www.python.org/downloads/). На Windows при установке отметьте «Add python.exe to PATH».
2. [Скачайте ZIP](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip), распакуйте и запустите:
   - Windows: двойной клик по `start-windows.bat`
   - macOS / Linux: `./start.sh`

   Первый запуск ставит зависимости, это займёт минуту. На macOS разрешите терминалу управление в «Системные настройки → Конфиденциальность и безопасность → Универсальный доступ», иначе он не сможет нажимать клавиши.
3. Дальше как в шагах 2–4 выше.

Ключ сохраняется, так что после перезапуска ПК повторно сканировать не нужно. Новый ключ (старые телефоны отключатся): `--reset-token`, например `start-windows.bat --reset-token`.

Программа на ПК пишет сообщения на языке системы, другой язык: `--lang en|ar|zh|ja|ru|de|gsw`.

`--console` запускает программу в терминале без окна, `--minimized` запускает сразу свёрнутой в трей.

## Как работает управление медиа

- **Пауза, следующее, предыдущее, громкость** работают через мультимедийные клавиши, поэтому доходят до того, что сейчас играет, даже если его окно не активно.
- **Перемотка и полный экран** нажимают стрелки и F, которые понимает большинство плееров, поэтому окно плеера должно быть активным. Если не срабатывают, откройте «Тачпад» и кликните по видео. **Скорость и субтитры** это горячие клавиши YouTube.

## Экран телефона

Чтобы экран не гас на дорожке, приложение пробует включить режим «экран не гаснет» (кнопка вверху). Браузеры разрешают это только по HTTPS, а пульт работает по обычному HTTP в домашней сети, поэтому на большинстве телефонов кнопка будет показывать «как в системе». Пока что увеличьте время отключения экрана в настройках телефона.

## Безопасность

Команды принимаются только от телефона с ключом из QR-кода. Ключ хранится в `%APPDATA%\pc-remote\token` (Windows) или `~/.pc-remote/token`. Трафик не шифруется, используйте пульт только в домашней сети. Как сообщить об уязвимости: [SECURITY.md](../SECURITY.md).

## Для разработчиков

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # команды пишутся в лог, клавиши не нажимаются
```

Структура:

- `pc_remote/actions.py`: какие клавиши нажимает каждая кнопка
- `pc_remote/app.py`: HTTP и WebSocket сервер, проверка сообщений
- `pc_remote/backend.py`: нажатия через pynput и тестовый режим
- `pc_remote/i18n.py`: сообщения программы на ПК на всех языках
- `pc_remote/static/`: приложение для телефона, переводы в `static/locales/`

Релизы: тег вида `v1.0.0` собирает `PocketTap-windows.exe` и публикует его на странице [Releases](https://github.com/universe-coder/pocket-tap/releases). Как добавить язык: [CONTRIBUTING.md](../CONTRIBUTING.md).

## Лицензия

[MIT](../LICENSE)
