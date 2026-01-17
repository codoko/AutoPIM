[app]

# (str) Title of your application
title = SYRT

# (str) Package name (unique identifier for your app)
package.name = inspectiontool

# (str) Package domain (e.g., org.example, com.yourcompany)
package.domain = org.example

# (str) Source code directory (where your main.py is located)
source.dir = .

# (list) Source files to include (defaults to all in source.dir)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
# This is crucial: it tells Buildozer what Python packages to include.
requirements = python3,kivy

# (str) Custom version
version = 1.0

# (str) Application versioning (method)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (list) Permissions
# We need these to access the phone's storage where your data files are.
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
# iOS section (not used for Android, can be ignored)
#

#
# Kivy section
#

# (bool) Enable debugging for the APK
debug = 1

# (str) The log level for the application
log_level = 2

# (str) Name of the .kv file (if you have one, otherwise leave empty)
# kv_file =

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# -----------------------------------------------------------------------------
# Profiles
#
# You can extend section / key with a profile
# For example, you want to deploy a demo version of your application without
# HD content. You could first change the title to add "(demo)" and extend
# the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug