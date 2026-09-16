[app]
# (str) Title of your application
title = ALERTX

# (str) Package name
package.name = alertx

# (str) Package domain (needed for android/ios packaging)
package.domain = com.alertx

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,png,jpg,json,ttf

# (str) Application versioning
version = 0.1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,https://github.com/kivymd/kivymd/archive/master.zip,materialyoucolor,materialshapes,asynckivy,plyer,pyjnius,pillow

# (str) python-for-android branch to use
p4a.branch = develop

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SEND_SMS,CALL_PHONE,READ_PHONE_STATE

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK / AAB will support
android.minapi = 26

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for (64-bit ARM for modern Android devices)
android.archs = arm64-v8a

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
