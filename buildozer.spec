[app]
# 应用名
title = PIMSystem
# 包名（按要求配置）
package.name = uexNormalPIM
package.domain = org.zywxv.wbpalmstar.widgetone
# 新增必填：应用版本（任意合法版本号均可）
version = 1.0.0
# 源码目录
source.dir = .
# 支持的文件后缀
source.include_exts = py,png,jpg,kv,atlas,txt,json
source.exclude_exts = spec,pyc,pyo
# 依赖库
requirements = python3,kivy==2.3.0,pathlib2
# 安卓权限（含高版本存储权限）
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
# 安卓版本配置
android.sdk = 24
android.ndk = 25b
android.api = 33
android.minapi = 21
android.buildtools = 33.0.2
# NDK/SDK 路径（GitHub Actions 用）
android.ndk_path = /home/runner/android-ndk-r25b
android.sdk_path = /home/runner/android-sdk
# 应用图标（可选，无则用默认）
icon.filename = icon.png
# 屏幕方向
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1