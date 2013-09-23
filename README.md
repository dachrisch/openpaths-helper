openpaths-helper
================

Tiny little helpers for playing around with OpenPaths API (https://openpaths.cc/api)

Instructions
============

1. Go to https://www.google.com/takeout/#custom:location_history and download your location data
2. Create an account at OpenPaths (https://openpaths.cc/)
3. Go to https://openpaths.cc/data and retrieve your *Access key* and *Secret key*
4. To upload your data, run the program as follows
```
upload_from_latitude.py <location_history.json> <access> <secret>
```

** You may need to install *oauth2* in your python environment. simply run
```
easy_install oauth2
```
in a shell