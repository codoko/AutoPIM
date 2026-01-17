[app]

title = PIM System
package.name = systempim
package.domain = com.example.pim

source.dir = .
source.include_exts = py

version = 1.0
requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1