[app]

# 应用基本信息
title = SYSPIM
package.name = inspection_tool
package.domain = org.yourdomain

# 源码目录
source.dir = .
source.include_exts = py,png,jpg,kv,txt,atlas

# 版本
version = 1.0

# 要求的 Python 版本和依赖
requirements = python==3.11.6, kivy==2.3.0

# Android 设置
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# 图标 (可选，如果没有，使用默认)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
