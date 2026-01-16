[app]
title = QuranKaremApp
package.name = qurankaremapp
package.domain = org.test
source.dir = .
source.include_exts = py,html,css,js,json,xml
version = 1.0

# المكتبات المطلوبة للتحميل (مهم جداً)
requirements = python3,kivy,pyjnius,requests,urllib3,certifi,idna,charset-normalizer

# صلاحيات الإنترنت والذاكرة (مهم جداً)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a