[app]

title = PIMSYS

package.name = xunjianauto

package.domain = org.example

source.dir = .

source.include_exts = py

requirements = python3,kivy

orientation = portrait

fullscreen = 1

# 必须设置版本名称（显示给用户看的，比如 1.0）
version = 1.0

# 推荐设置版本代码（Android 内部用整数，必须递增，以后升级 APK 时改成 2、3...）
numeric_version = 1

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 34

android.minapi = 21

android.sdk = 34

android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2