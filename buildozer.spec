[app]

title = 巡检自动化工具
package.name = xunjianauto
package.domain = com.example

source.dir = .
source.include_exts = py

version = 1.0
requirements = python3,kivy==2.2.1

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 自动接受所有 SDK 许可证（解决无交互环境下的许可证问题）
android.accept_sdk_license = true

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1