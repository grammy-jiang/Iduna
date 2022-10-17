"""
A configurable set of panels that display various debug information about the current
request/response.

* https://github.com/jazzband/django-debug-toolbar
"""
from ..django import INSTALLED_APPS, INTERNAL_IPS, MIDDLEWARE

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS.append("127.0.0.1")
