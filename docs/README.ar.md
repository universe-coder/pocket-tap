<div dir="rtl">

# PocketTap

[English](../README.md) · **العربية** · [中文](README.zh.md) · [日本語](README.ja.md) · [Русский](README.ru.md) · [Deutsch / Schweiz](README.de.md)

حوِّل هاتفك إلى جهاز تحكم عن بُعد لجهاز الكمبيوتر عبر شبكة Wi-Fi المنزلية. الاستخدام الأول: مشاهدة YouTube على الكمبيوتر أثناء المشي على جهاز المشي، والتحكم في الفيديو من الهاتف.

[![تنزيل لنظام Windows](https://img.shields.io/badge/%D8%AA%D9%86%D8%B2%D9%8A%D9%84-Windows%20(.exe)-2ea44f?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe)
[![تنزيل ZIP لنظامي macOS وLinux](https://img.shields.io/badge/%D8%AA%D9%86%D8%B2%D9%8A%D9%84-macOS%20%2F%20Linux%20(.zip)-555?style=for-the-badge&logo=github)](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip)

[![Release](https://img.shields.io/github/v/release/universe-coder/pocket-tap?label=release&color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/universe-coder/pocket-tap/total?color=2ea44f)](https://github.com/universe-coder/pocket-tap/releases)
[![tests](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/universe-coder/pocket-tap/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/github/license/universe-coder/pocket-tap?color=blue)](../LICENSE)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational)
![Phone](https://img.shields.io/badge/phone-Android%20%7C%20iPhone-informational)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python&logoColor=white)
![Languages](https://img.shields.io/badge/languages-EN%20%7C%20AR%20%7C%20ZH%20%7C%20JA%20%7C%20RU%20%7C%20DE%20%7C%20CH-orange)
[![Stars](https://img.shields.io/github/stars/universe-coder/pocket-tap?style=social)](https://github.com/universe-coder/pocket-tap/stargazers)

## لقطات الشاشة

<table>
<tr><td align="center"><img src="screenshots/phone-media.png" width="180" alt="الوسائط"><br><sub>الوسائط</sub></td><td align="center"><img src="screenshots/phone-touchpad.png" width="180" alt="لوحة اللمس"><br><sub>لوحة اللمس</sub></td><td align="center"><img src="screenshots/phone-keyboard.png" width="180" alt="لوحة المفاتيح"><br><sub>لوحة المفاتيح</sub></td></tr>
<tr><td align="center"><img src="screenshots/phone-arabic.png" width="180" alt="العربية، من اليمين إلى اليسار"><br><sub>العربية، من اليمين إلى اليسار</sub></td><td align="center"><img src="screenshots/phone-japanese.png" width="180" alt="اليابانية"><br><sub>اليابانية</sub></td><td></td></tr>
</table>

<p align="center"><img src="screenshots/pc-window.png" width="520" alt="برنامج الكمبيوتر: امسح رمز QR بهاتفك"><br><sub>برنامج الكمبيوتر: امسح رمز QR بهاتفك</sub></p>

يتكوّن من جزأين:

- **برنامج الكمبيوتر** (`pc_remote`، بلغة Python): يضغط المفاتيح ويحرّك الفأرة وفق أوامر الهاتف. المنصة الأساسية هي Windows، ويعمل أيضًا على macOS وLinux (X11).
- **تطبيق الهاتف**: تطبيق ويب (PWA) يقدّمه الكمبيوتر نفسه عبر Wi-Fi. لا حاجة إلى التثبيت من متجر التطبيقات: امسح رمز QR، ويمكنك إضافته إلى الشاشة الرئيسية ليُفتح كتطبيق عادي. يعمل على Android وiPhone.

يدعم تطبيق الهاتف الإنجليزية والعربية (من اليمين إلى اليسار) والصينية واليابانية والروسية والألمانية والألمانية السويسرية. يتبع لغة الهاتف تلقائيًا، ويمكن تغييرها من أعلى الشاشة.

## الميزات

**الوسائط**: تعمل مع أي مشغّل (YouTube وNetflix وSpotify وVLC وغيرها): زر كبير للإيقاف المؤقت والتشغيل، ترجيع وتقديم (اضغط مطولًا للاستمرار)، التالي والسابق، مستوى صوت النظام، ملء الشاشة. وفي YouTube أيضًا سرعة التشغيل والترجمة.

**لوحة اللمس**: تحريك المؤشر بالإصبع، النقر بلمسة، النقر الأيمن بلمسة بإصبعين، التمرير بإصبعين، وأزرار الرجوع والتقدم والتحديث للمتصفح.

**لوحة المفاتيح**: كتابة نص على الكمبيوتر (مثل البحث في YouTube)، وEnter وEsc والأسهم ومفاتيح أخرى.

**نافذة الكمبيوتر**: رمز QR، واختيار الشبكة (إذا تعذّر اتصال الهاتف فاختر الشبكة التي يتصل بها، عادةً Wi-Fi)، وقائمة الهواتف المتصلة، والسجل. عند إغلاق النافذة يستمر PocketTap في العمل في علبة النظام على Windows (وتُصغَّر النافذة على macOS وLinux)؛ وللإنهاء استخدم قائمة أيقونة العلبة. يتحقق البرنامج من وجود إصدار جديد على GitHub ويعرض تنزيله.

## البدء

### Windows: ملف واحد دون الحاجة إلى Python

1. نزِّل [PocketTap-windows.exe](https://github.com/universe-coder/pocket-tap/releases/latest/download/PocketTap-windows.exe) وشغّله.
   قد يحذّر Windows من ناشر غير معروف لأن البرنامج غير موقّع رقميًا: انقر **مزيد من المعلومات** ثم **تشغيل على أي حال**.
2. عندما يسأل Windows عن الوصول إلى الشبكة، اسمح به **للشبكات الخاصة**.
3. سيظهر رمز QR في النافذة. امسحه بكاميرا الهاتف، ويجب أن يكون الهاتف على شبكة Wi-Fi نفسها.
4. لفتح جهاز التحكم بلمسة واحدة: من قائمة متصفح الهاتف اختر «إضافة إلى الشاشة الرئيسية».

### أي نظام، باستخدام Python

1. ثبّت [Python 3.9+](https://www.python.org/downloads/). على Windows فعّل خيار «Add python.exe to PATH» أثناء التثبيت.
2. [نزِّل ملف ZIP](https://github.com/universe-coder/pocket-tap/archive/refs/heads/main.zip) وفُكّ ضغطه وشغّل:
   - Windows: انقر نقرًا مزدوجًا على `start-windows.bat`
   - macOS / Linux: `./start.sh`

   التشغيل الأول يثبّت المكتبات اللازمة ويستغرق نحو دقيقة. على macOS اسمح للطرفية (Terminal) من «إعدادات النظام ← الخصوصية والأمن ← تسهيلات الاستخدام» حتى تتمكن من ضغط المفاتيح.
3. ثم تابع من الخطوة 2 أعلاه.

يُحفظ مفتاح الاقتران، فلا حاجة إلى المسح من جديد بعد إعادة تشغيل الكمبيوتر. لإصدار مفتاح جديد (ستنقطع الهواتف القديمة): `--reset-token`، مثلًا `start-windows.bat --reset-token`.

يعرض برنامج الكمبيوتر رسائله بلغة النظام؛ ولاختيار لغة أخرى استخدم `--lang en|ar|zh|ja|ru|de|gsw`.

استخدم `--console` للعمل في الطرفية بدل النافذة، و`--minimized` للبدء مخفيًا في علبة النظام.

## كيف يعمل التحكم في الوسائط

- **الإيقاف المؤقت والتالي والسابق ومستوى الصوت** تعمل عبر مفاتيح الوسائط، لذلك تصل إلى ما يُشغَّل حتى لو لم تكن نافذته نشطة.
- **الترجيع والتقديم وملء الشاشة** تضغط مفاتيح الأسهم وF التي تفهمها معظم المشغّلات، لذلك يجب أن تكون نافذة المشغّل نشطة. إذا لم تعمل، افتح «لوحة اللمس» وانقر على الفيديو. **السرعة والترجمة** اختصارات في YouTube.

## شاشة الهاتف

حتى لا تنطفئ الشاشة أثناء المشي، يحاول التطبيق تفعيل «إبقاء الشاشة مضاءة» (الزر في الأعلى). تسمح المتصفحات بذلك فقط عبر HTTPS، بينما يعمل جهاز التحكم عبر HTTP العادي داخل الشبكة المنزلية، لذا سيعرض الزر في معظم الهواتف «حسب النظام». إلى ذلك الحين، زِد مدة انطفاء الشاشة من إعدادات الهاتف.

## الأمان

لا تُقبل الأوامر إلا من هاتف يحمل المفتاح الموجود في رمز QR. يُحفظ المفتاح في `%APPDATA%\pc-remote\token` (على Windows) أو `~/.pc-remote/token`. الاتصال غير مشفّر، لذا استخدم جهاز التحكم داخل شبكتك المنزلية فقط. للإبلاغ عن ثغرة أمنية راجع [SECURITY.md](../SECURITY.md).

## للمطوّرين

</div>

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # log commands instead of pressing keys
```

<div dir="rtl">

البنية:

- `pc_remote/actions.py`: المفاتيح التي يضغطها كل زر
- `pc_remote/app.py`: خادم HTTP وWebSocket والتحقق من الرسائل
- `pc_remote/backend.py`: ضغط المفاتيح عبر pynput ووضع الاختبار
- `pc_remote/i18n.py`: رسائل برنامج الكمبيوتر بجميع اللغات
- `pc_remote/static/`: تطبيق الهاتف، والترجمات في `static/locales/`

الإصدارات: دفع وسم مثل `v1.0.0` يبني `PocketTap-windows.exe` وينشره في صفحة [Releases](https://github.com/universe-coder/pocket-tap/releases). لإضافة لغة جديدة راجع [CONTRIBUTING.md](../CONTRIBUTING.md).

## الترخيص

[MIT](../LICENSE)

</div>
