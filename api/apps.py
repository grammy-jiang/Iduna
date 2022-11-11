"""Configure the application of api

* https://docs.djangoproject.com/en/4.1/ref/applications/
"""
from apps import AppConfig


class ApiConfig(AppConfig):
    """the configuration of the application of api"""

    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
