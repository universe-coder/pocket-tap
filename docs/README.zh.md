# TapRemote

[English](../README.md) · [العربية](README.ar.md) · **中文** · [日本語](README.ja.md) · [Русский](README.ru.md) · [Deutsch / Schweiz](README.de.md)

通过家里的 Wi-Fi，把手机变成电脑的遥控器。最初的场景：在跑步机上用电脑看 YouTube，用手机控制视频。

[![下载 Windows 版](https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD-Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/universe-coder/pocket-tap/releases/latest/download/TapRemote-windows.exe)
[![下载 macOS / Linux 版 ZIP](https://img.shields.io/badge/%E4%B8%8B%E8%BD%BD-macOS%20%2F%20Linux%20(.zip)-555?style=for-the-badge&logo=github)](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)

由两部分组成：

- **电脑端程序**（`pc_remote`，Python）：根据手机发来的指令按键和移动鼠标。主要平台是 Windows，也支持 macOS 和 Linux（X11）。
- **手机端应用**：由电脑通过 Wi-Fi 直接提供的网页应用（PWA）。无需从应用商店安装：扫描二维码即可使用，也可以添加到主屏幕，像普通应用一样打开。支持 Android 和 iPhone。

手机端支持英语、阿拉伯语（从右到左）、中文、日语、俄语、德语和瑞士德语。默认跟随手机语言，也可以在屏幕顶部切换。

## 功能

**YouTube**：大号暂停/播放按钮，快退/快进 10 秒（按住可连续快进），上一个和下一个视频，系统音量，播放速度，字幕，全屏。

**触控板**：手指移动光标，轻点单击，双指轻点右键，双指滚动，以及浏览器的后退、前进、刷新按钮。

**键盘**：在电脑上输入文字（例如在 YouTube 搜索），Enter、Esc、方向键等按键。

## 开始使用

### Windows：单个文件，无需 Python

1. 下载 [TapRemote-windows.exe](https://github.com/universe-coder/pocket-tap/releases/latest/download/TapRemote-windows.exe) 并运行。
   由于程序没有代码签名，Windows 可能会提示"未知发布者"：点击**更多信息**，然后点击**仍要运行**。
2. Windows 询问网络访问权限时，允许**专用网络**。
3. 窗口中会出现二维码。用手机相机扫描，手机需要连接同一个 Wi-Fi。
4. 想一键打开遥控器：在手机浏览器菜单中选择"添加到主屏幕"。

### 任意系统，使用 Python

1. 安装 [Python 3.9+](https://www.python.org/downloads/)。在 Windows 上安装时勾选 "Add python.exe to PATH"。
2. [下载 ZIP](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)，解压后运行：
   - Windows：双击 `start-windows.bat`
   - macOS / Linux：`./start.sh`

   首次运行会安装依赖，大约需要一分钟。在 macOS 上，请在"系统设置 → 隐私与安全性 → 辅助功能"中允许终端，否则无法模拟按键。
3. 之后按照上面的第 2 至 4 步操作。

配对密钥会被保存，重启电脑后无需重新扫描。生成新密钥（旧手机将断开）：`--reset-token`，例如 `start-windows.bat --reset-token`。

电脑端程序使用系统语言显示消息；可用 `--lang en|ar|zh|ja|ru|de|gsw` 指定其他语言。

## 开启 VPN 时

遥控器在家庭网络内直接从手机连接电脑，不需要 VPN。但电脑或手机上的 VPN 可能会造成干扰。

**电脑上的 VPN。** 程序会选择家庭网络地址（如 192.168.x.x），而不是 VPN 地址，并在二维码下方列出电脑的其他地址。如果手机打不开页面，请用列表中的其他地址启动：`--ip 192.168.1.42`。如果 VPN 有"允许局域网"（Allow LAN / Local network sharing）之类的设置，请开启：否则某些带 kill switch 的 VPN 会阻止来自家庭网络的连接。

**手机上的 VPN。** VPN 常常把访问家庭网络的流量也送进隧道。请在 VPN 应用中开启局域网例外：
- v2rayNG、Hiddify、NekoBox、Clash：路由设置中的"绕过局域网"（Bypass LAN）
- Amnezia、Outline 等支持分流的应用：把浏览器（或遥控器应用）加入例外
- WireGuard：在隧道中开启"排除私有 IP"（Exclude private IPs）
- Android：如果开启了"屏蔽未使用 VPN 的连接"，遥控器将无法工作，请关闭该选项或使用上面的例外设置

## YouTube 控制原理

- **暂停、上一个、下一个和音量**使用多媒体键，即使浏览器窗口不在前台也能生效。
- **快进快退、速度、字幕和全屏**是 YouTube 快捷键，需要视频标签页处于焦点。如果没有反应，请打开"触控板"并点击一下视频。

## 手机屏幕

为了在跑步机上保持屏幕常亮，应用会尝试开启"屏幕常亮"（顶部按钮）。浏览器只允许在 HTTPS 下这样做，而遥控器在家庭网络中使用普通 HTTP，所以大多数手机上按钮会显示"跟随系统"。暂时请在手机设置中延长自动锁屏时间。

## 安全

只接受持有二维码中密钥的手机发来的指令。密钥保存在 `%APPDATA%\pc-remote\token`（Windows）或 `~/.pc-remote/token`。通信未加密，请只在家庭网络中使用。报告漏洞请见 [SECURITY.md](../SECURITY.md)。

## 开发者

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # 只记录指令，不实际按键
```

结构：

- `pc_remote/actions.py`：每个按钮对应的按键
- `pc_remote/app.py`：HTTP 和 WebSocket 服务器，消息校验
- `pc_remote/backend.py`：通过 pynput 按键，以及测试模式
- `pc_remote/i18n.py`：电脑端程序各语言的消息
- `pc_remote/static/`：手机端应用，翻译位于 `static/locales/`

发布：推送 `v1.0.0` 这样的标签会构建 `TapRemote-windows.exe` 并发布到 [Releases](https://github.com/universe-coder/pocket-tap/releases) 页面。添加新语言请见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 许可证

[MIT](../LICENSE)
