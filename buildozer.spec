[app]

# (str) Title of your application
title = 巡检助手

# (str) Package name (unique identifier for your app)
package.name = inspectiontool

# (str) Package domain (e.g., org.example, com.yourcompany)
package.domain = org.example

# (str) Source code directory (where your main.py is located)
source.dir = .

# (list) Source files to include (defaults to all in source.dir)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy

# (str) Custom version - FIXED VERSION
version = 1.0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API level to use
android.api = 31

# (int) Minimum Android API level supported
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (bool) Enable AndroidX support
android.enable_androidx = True

#
# Kivy section
#
debug = 1
log_level = 2

# (End of file)