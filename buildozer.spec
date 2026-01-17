[app]

title = 巡检自动化工具
package.name = xunjianauto
package.domain = com.example

source.dir = .
source.include_exts = py

version = 1.0
requirements = python3,kivy  # 移除版本锁定，使用最新兼容 Kivy

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = true

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# 为 Android 10+ 启用 legacy external storage（确保访问 /storage/emulated/0 路径）
android.extra_manifest_application = android:requestLegacyExternalStorage="true"

[buildozer]

log_level = 2
warn_on_root = 1