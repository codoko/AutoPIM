[app]

# (str) Title of your application
title = PIM

# (str) Package name
package.name = inspectionapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.inspection

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy==2.2.1,python-dateutil

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin

#    ----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to be added to the list
#    format.
#    Check buildozer docs for more information.
#    ----------------------------------------------------------------------------

# (list) Android specific

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (list) The Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app. Can be one of: apk, aab
android.package_format = apk

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you are registering in
# android.add_jars so that pyjnius can access their classes.
android.add_jars = 

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
android.add_src = 

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
android.add_aars = 

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# bootstrap)
android.gradle_dependencies = 

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the
# 'android.gradle_dependencies' option
# See https://developer.android.com/studio/write/java8-support for
# information about using Java 8 language features
#android.add_compile_options = 

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.add_gradle_repositories = 

# (list) packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts
#android.add_packaging_options = 

# (list) Java classes to add as activities to the android manifest.
#android.add_activities = com.example.ExampleActivity

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest_placeholders = 

# (str) Splash screen image
#android.presplash_lottie = 

# (str) AdMob App ID
#android.admob_app_id = 

# (bool) Enable debug mode for the Android build
#android.debug = True

# (str) The type of ads to show in the AdMob banner
#android.admob_banner_ad_type = BANNER

# (str) The ad unit id for the AdMob banner
#android.admob_banner_ad_unit_id = 

# (str) The ad unit id for the AdMob interstitial
#android.admob_interstitial_ad_unit_id = 

# (str) The ad unit id for the AdMob rewarded video
#android.admob_rewarded_video_ad_unit_id = 

# (str) The ad unit id for the AdMob native advanced
#android.admob_native_ad_unit_id = 

# (bool) (Android) Skip the automatic update of the Android SDK
#android.skip_update = False

# (bool) (Android) Automatically accept the SDK license agreements
#android.accept_sdk_license = True

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk

# (str) (Android) The format used to package the app. Can be one of: apk, aab
# android.package_format = apk