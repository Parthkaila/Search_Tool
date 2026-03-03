[app]
title = Maps Collector
package.name = mapscollector
package.domain = org.mapscollector

source.dir = .
source.include_exts = py,png,jpg

version = 0.1

requirements = python3,kivy,requests

orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
