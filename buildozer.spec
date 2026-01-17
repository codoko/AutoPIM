[app]
# 应用名改为 PIMSystem
title = PIMSystem
# 包名改为指定的 org.zywxv.wbpalmstar.widgetone.uexNormalPIM
package.name = uexNormalPIM
package.domain = org.zywxv.wbpalmstar.widgetone
# 源码目录（不变）
source.dir = .
# 支持的文件后缀（包含脚本所需的 txt/json）
source.include_exts = py,png,jpg,kv,atlas,txt,json
source.exclude_exts = spec,pyc,pyo
# 依赖库（保持与 main.py 匹配）
requirements = python3,kivy==2.3.0,pathlib2
# 安卓权限（确保能读写原目录文件）
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
# 安卓版本配置（兼容主流设备）
android.sdk = 24
android.ndk = 25b
android.api = 33
android.minapi = 21
android.buildtools = 33.0.2
# NDK/SDK 路径（GitHub Actions 构建用）
android.ndk_path = /home/runner/android-ndk-r25b
android.sdk_path = /home/runner/android-sdk
# 应用图标（可选，无图标则用默认）
icon.filename = icon.png
# 屏幕适配
orientation = portrait