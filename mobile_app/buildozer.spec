[app]
title = Google Maps Collector
package.name = mapscollector
package.domain = com.mapsscraper

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,requests,pandas,openpyxl,jnius

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Android API level
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# App icon (optional, create icon.png)
#icon.filename = %(source.dir)s/icon.png

# Presplash (optional)
#presplash.filename = %(source.dir)s/presplash.png

# Supported architectures
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
