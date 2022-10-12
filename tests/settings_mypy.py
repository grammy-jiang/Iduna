"""
the settings only for mypy
"""
import django_stubs_ext

from config.settings import *  # pylint: disable=wildcard-import,unused-wildcard-import

django_stubs_ext.monkeypatch()
