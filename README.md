# TapRemote

**English** · [العربية](docs/README.ar.md) · [中文](docs/README.zh.md) · [日本語](docs/README.ja.md) · [Русский](docs/README.ru.md) · [Deutsch / Schweiz](docs/README.de.md)

Turn your phone into a remote control for your PC over home Wi-Fi. Built for watching YouTube on the computer while on a treadmill, and controlling the video from the phone.

[![Download for Windows](https://img.shields.io/badge/Download-Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/universe-coder/pocket-tap/releases/latest/download/TapRemote-windows.exe)
[![Download ZIP for macOS and Linux](https://img.shields.io/badge/Download-macOS%20%2F%20Linux%20(.zip)-555?style=for-the-badge&logo=github)](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)

[![tests](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Two parts:

- **The PC program** (`pc_remote`, Python) presses keys and moves the mouse on commands from the phone. Windows is the main platform; macOS and Linux (X11) work too.
- **The phone app** is a web app (PWA) that the PC serves over Wi-Fi. Nothing to install from an app store: scan a QR code and optionally add it to the home screen, where it opens like a regular app. Works on Android and iPhone.

The phone app speaks English, Arabic (right to left), Chinese, Japanese, Russian, German and Swiss German. It follows the phone's language, and you can switch it at the top of the screen.

## Features

**YouTube**: a big play/pause button, seek ±10 seconds (hold to keep seeking), next and previous video, system volume, playback speed, captions, full screen.

**Touchpad**: move the cursor with a finger, tap to click, two-finger tap to right-click, two-finger scroll, and Back, Forward and Refresh buttons for the browser.

**Keyboard**: type text on the PC (for example, a YouTube search), Enter, Esc, arrows and other keys.

## Getting started

### Windows: one file, no Python needed

1. Download [TapRemote-windows.exe](https://github.com/universe-coder/pocket-tap/releases/latest/download/TapRemote-windows.exe) and run it.
   Windows may warn about an unknown publisher because the program is not code-signed: click **More info**, then **Run anyway**.
2. When Windows asks about network access, allow it for **private networks**.
3. A QR code appears in the window. Scan it with your phone camera; the phone must be on the same Wi-Fi.
4. To open the remote with one tap, add it to the home screen from the phone browser's menu.

### Any system, with Python

1. Install [Python 3.9+](https://www.python.org/downloads/). On Windows, tick "Add python.exe to PATH" during setup.
2. [Download the ZIP](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip), unpack it and run:
   - Windows: double-click `start-windows.bat`
   - macOS / Linux: `./start.sh`

   The first run installs dependencies, which takes about a minute. On macOS, allow the terminal under System Settings → Privacy & Security → Accessibility so it can press keys.
3. Continue from step 2 above.

The pairing key is saved, so you don't need to scan again after restarting the PC. To issue a new key (old phones get disconnected): `--reset-token`, for example `start-windows.bat --reset-token`.

The PC program prints its messages in the system language; choose another one with `--lang en|ar|zh|ja|ru|de|gsw`.

## If a VPN is on

The remote talks directly from the phone to the PC inside your home network and doesn't need the VPN. A VPN on either the PC or the phone can get in the way.

**VPN on the PC.** The program picks the home network address (192.168.x.x and the like) rather than the VPN one, and prints the PC's other addresses under the QR code. If the phone can't open the page, start it with another address from that list: `--ip 192.168.1.42`. If your VPN has a setting like "Allow LAN" or "Local network sharing", turn it on: without it some VPNs (with a kill switch) block incoming connections from the home network.

**VPN on the phone.** VPN apps often send home network traffic into the tunnel too. Turn on the local network exception in the VPN app:
- v2rayNG, Hiddify, NekoBox, Clash: "Bypass LAN" in the routing settings
- Amnezia, Outline and others with split tunneling: add the browser (or the remote app) to the exceptions
- WireGuard: enable "Exclude private IPs" for the tunnel
- Android: if "Block connections without VPN" is on, the remote can't work; turn it off or use the exceptions above

## How YouTube control works

- **Play/pause, next, previous and volume** use media keys, so they work even when the browser window isn't focused.
- **Seeking, speed, captions and full screen** are YouTube hotkeys and need the video tab focused. If they do nothing, open the Touchpad tab and click the video.

## Phone screen

To keep the screen on while you're on the treadmill, the app tries to enable "keep screen on" (the button at the top). Browsers only allow that over HTTPS, while the remote uses plain HTTP inside the home network, so on most phones the button shows "system setting". Until then, raise the screen timeout in the phone's settings.

## Security

Commands are accepted only from a phone with the key from the QR code. The key is stored in `%APPDATA%\pc-remote\token` (Windows) or `~/.pc-remote/token`. Traffic is not encrypted: use the remote only on your home network. See [SECURITY.md](SECURITY.md) to report a vulnerability.

## For developers

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # log commands instead of pressing keys
```

Layout:

- `pc_remote/actions.py`: which keys each button presses
- `pc_remote/app.py`: HTTP and WebSocket server, message validation
- `pc_remote/backend.py`: key presses through pynput, and the dry-run mode
- `pc_remote/i18n.py`: the PC program's messages in every language
- `pc_remote/static/`: the phone app; translations live in `static/locales/`

Releases: pushing a tag such as `v1.0.0` builds `TapRemote-windows.exe` and publishes it on the [Releases](https://github.com/universe-coder/pocket-tap/releases) page. See [CONTRIBUTING.md](CONTRIBUTING.md), including how to add a language.

## License

[MIT](LICENSE)
