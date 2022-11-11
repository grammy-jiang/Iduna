"""Configure the application of aria2

* https://docs.djangoproject.com/en/4.1/ref/applications/
"""
from apps import AppConfig


class Aria2Config(AppConfig):
    """the configuration of the application of aria2"""

    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "aria2"
