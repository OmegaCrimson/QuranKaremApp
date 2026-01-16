[app]

# (str) Title of your application
title = MyHTMLApp

# (str) Package name
package.name = myhtmlapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (str) Source code filename (let's keep it simple)
source.include_exts = py,html,css,js

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,pyjnius

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible (currently 34)
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 24

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY