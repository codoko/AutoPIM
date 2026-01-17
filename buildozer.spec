[app]
title = 自动化巡检
package.name = inspection_tool
package.domain = org.auto.inspect
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0.0

# [span_0](start_span)核心依赖[span_0](end_span)
requirements = python3,kivy

# 屏幕方向
orientation = portrait

# [span_1](start_span)重点：Android 权限申请[span_1](end_span)
# 必须包含读写权限才能处理 /storage/emulated/0/ 下的文件
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Android API 级别 (建议保持 33 或 34)
android.api = 33
android.minapi = 21
android.sdk = 33

# 是否全屏
fullscreen = 0

# (以下为构建环境配置，保持默认即可)
[buildozer]
log_level = 2
warn_on_root = 1