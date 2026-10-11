<p align="center"><img src="../pc_remote/static/icon.svg" width="128" alt="PocketTap"></p>

<h1 align="center">PocketTap</h1>

[English](../README.md) · [العربية](README.ar.md) · [中文](README.zh.md) · **日本語** · [Русский](README.ru.md) · [Deutsch / Schweiz](README.de.md)

自宅の Wi-Fi で、スマートフォンを PC のリモコンにします。最初の用途：ランニングマシンの上で PC の YouTube を見ながら、スマートフォンで動画を操作すること。

[![Windows 版をダウンロード](https://img.shields.io/badge/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89-Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe)
[![macOS / Linux 版 ZIP をダウンロード](https://img.shields.io/badge/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89-macOS%20%2F%20Linux%20(.zip)-555?style=for-the-badge&logo=github)](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)

[![Release](https://img.shields.io/github/v/release/universe-coder/pocket-tap?label=release&color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/universe-coder/pocket-tap/total?color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases)
[![tests](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/github/license/universe-coder/pocket-tap?color=blue)](../LICENSE)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational)
![Phone](https://img.shields.io/badge/phone-Android%20%7C%20iPhone-informational)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Languages](https://img.shields.io/badge/languages-EN%20%7C%20AR%20%7C%20ZH%20%7C%20JA%20%7C%20RU%20%7C%20DE%20%7C%20CH-orange)
[![Stars](https://img.shields.io/github/stars/universe-coder/pocket-tap?style=social)](https://github.com/universe-coder/pocket-tap/stargazers)

## スクリーンショット

<table>
<tr><td align="center"><img src="screenshots/phone-media.png" width="180" alt="メディア"><br><sub>メディア</sub></td><td align="center"><img src="screenshots/phone-touchpad.png" width="180" alt="タッチパッド"><br><sub>タッチパッド</sub></td><td align="center"><img src="screenshots/phone-keyboard.png" width="180" alt="キーボード"><br><sub>キーボード</sub></td></tr>
<tr><td align="center"><img src="screenshots/phone-arabic.png" width="180" alt="アラビア語（右から左）"><br><sub>アラビア語（右から左）</sub></td><td align="center"><img src="screenshots/phone-japanese.png" width="180" alt="日本語"><br><sub>日本語</sub></td><td></td></tr>
</table>

<p align="center"><img src="screenshots/pc-window.png" width="520" alt="PC 用プログラム：スマートフォンで QR コードを読み取ります"><br><sub>PC 用プログラム：スマートフォンで QR コードを読み取ります</sub></p>

2 つの部分からなります：

- **PC 用プログラム**（`pc_remote`、Python）：スマートフォンからの指示でキーを押し、マウスを動かします。メインは Windows で、macOS と Linux（X11）でも動作します。
- **スマートフォン用アプリ**：PC が Wi-Fi で直接配信する Web アプリ（PWA）です。ストアからのインストールは不要：QR コードを読み取るだけで使え、ホーム画面に追加すれば普通のアプリのように開けます。Android と iPhone に対応。

スマートフォン用アプリは英語、アラビア語（右から左）、中国語、日本語、ロシア語、ドイツ語、スイスドイツ語に対応しています。スマートフォンの言語に合わせて表示され、画面上部で切り替えることもできます。

## できること

**メディア**：どのプレーヤーでも使えます（YouTube、Netflix、Spotify、VLC など）。大きな一時停止/再生ボタン、巻き戻し・早送り（長押しで連続）、前へ・次へ、システム音量、全画面。YouTube では再生速度と字幕も操作できます。

**タッチパッド**：指でカーソル移動、タップでクリック、2 本指タップで右クリック、2 本指スクロール、ブラウザの「戻る」「進む」「更新」ボタン。

**キーボード**：PC への文字入力（YouTube の検索など）、Enter、Esc、矢印キーなど。

**PC のウィンドウ**：QR コード、ネットワークの選択（スマートフォンが接続できない場合は、つながっているネットワーク（通常は Wi-Fi）を選択）、接続中のスマートフォンの一覧、ログ。ウィンドウを閉じても、Windows では PocketTap がトレイで動作し続けます（macOS と Linux では最小化されます）。終了はトレイアイコンのメニューから。新しいバージョンを GitHub で確認し、ダウンロードを案内します。

## 使い方

### Windows：ファイル 1 つ、Python 不要

1. [PocketTap-windows.exe](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe) をダウンロードして実行します。
   プログラムにコード署名がないため、Windows が「不明な発行元」と警告することがあります：**詳細情報**をクリックし、**実行**を選んでください。
2. Windows がネットワークへのアクセスを確認したら、**プライベート ネットワーク**で許可します。
3. ウィンドウに QR コードが表示されます。スマートフォンのカメラで読み取ってください。スマートフォンは同じ Wi-Fi に接続している必要があります。
4. ワンタップで開けるようにするには、ホーム画面に追加します。リモコンの画面にお使いのスマホ向けの手順が表示されます。アイコンから開くとペアリング済みの状態で起動し、iPhone では普通のアプリのように動き、Android では最初のタップで全画面になります（HTTPS なしの Wi-Fi では Android のブラウザは完全なインストールを許可しません）。

### どの OS でも、Python で

1. [Python 3.9+](https://www.python.org/downloads/) をインストールします。Windows ではインストール時に「Add python.exe to PATH」にチェックを入れてください。
2. [ZIP をダウンロード](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)して展開し、実行します：
   - Windows：`start-windows.bat` をダブルクリック
   - macOS / Linux：`./start.sh`

   初回は依存関係をインストールするため 1 分ほどかかります。macOS では「システム設定 → プライバシーとセキュリティ → アクセシビリティ」でターミナルを許可してください。許可しないとキーを押せません。
3. あとは上の手順 2〜4 と同じです。

ペアリングキーは保存されるので、PC を再起動しても読み取り直す必要はありません。新しいキーを発行するには（古いスマートフォンは切断されます）：`--reset-token`、例：`start-windows.bat --reset-token`。

PC 用プログラムはシステムの言語でメッセージを表示します。別の言語にするには `--lang en|ar|zh|ja|ru|de|gsw` を指定します。

ウィンドウの代わりにターミナルを使うには `--console`、トレイに隠れた状態で起動するには `--minimized` を指定します。

## メディア操作のしくみ

- **一時停止/再生・次へ・前へ・音量**はメディアキーを使うので、再生中のアプリのウィンドウがアクティブでなくても届きます。
- **巻き戻し・早送り・全画面**はほとんどのプレーヤーが対応している矢印キーと F キーを押すため、プレーヤーのウィンドウがアクティブである必要があります。反応しない場合は「タッチパッド」を開いて動画をクリックしてください。**速度と字幕**は YouTube のショートカットキーです。

## スマートフォンの画面

ランニング中に画面が消えないよう、アプリは「画面を常にオン」を試みます（上部のボタン）。ブラウザはこれを HTTPS でしか許可しませんが、リモコンは自宅ネットワーク内で通常の HTTP を使うため、多くのスマートフォンではボタンが「システム設定」と表示されます。当面は、スマートフォンの設定で画面がオフになるまでの時間を長くしてください。

## セキュリティ

QR コードのキーを持つスマートフォンからの指示だけを受け付けます。キーは `%APPDATA%\pc-remote\token`（Windows）または `~/.pc-remote/token` に保存されます。通信は暗号化されないため、自宅のネットワーク内でのみ使ってください。脆弱性の報告は [SECURITY.md](../SECURITY.md) を参照してください。

## 開発者向け

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # キーを押さずに指示をログに出力
```

構成：

- `pc_remote/actions.py`：各ボタンが押すキー
- `pc_remote/app.py`：HTTP と WebSocket のサーバー、メッセージの検証
- `pc_remote/backend.py`：pynput によるキー操作とテストモード
- `pc_remote/i18n.py`：PC 用プログラムの各言語のメッセージ
- `pc_remote/static/`：スマートフォン用アプリ。翻訳は `static/locales/` にあります

リリース：`v1.0.0` のようなタグを push すると `PocketTap-windows.exe` がビルドされ、[Releases](https://github.com/universe-coder/pocket-tap/releases) ページで公開されます。言語の追加方法は [CONTRIBUTING.md](../CONTRIBUTING.md) を参照してください。

## ライセンス

[MIT](../LICENSE)
