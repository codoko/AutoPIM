[app]

# App 基本信息
title = 巡检自动化
package.name = inspection
package.domain = com.inspection.auto
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json
version = 1.0.0

# 依赖
requirements = python3,kivy

# Android 配置
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.storage_permissions = True

# 全屏模式
fullscreen = 0
orientation = portrait

# 图标 & 启动画面 (可替换)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# 日志级别
log_level = 2

# P4A (python-for-android) recipe
p4a.branch = develop

[buildozer]
warn_on_root = 0
