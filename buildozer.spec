[app]
title = ExtraTag Phone
package.name = extratagphone
package.domain = org.extratag
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
source.include_patterns = Extratag_Email/*,Extratag_Vcall/*
version = 0.1

# הגדרה מדויקת של הדרישות לקוד שלך
requirements = python3,kivy==2.3.0,pyjnius

orientation = portrait
fullscreen = 0

# הגדרות אנדרואיד
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# גרסת p4a יציבה שתואמת ל-pyjnius
p4a.branch = release-2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
