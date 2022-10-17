"""
The admin of Aria2 model of aria2
"""
from django.contrib import admin

from aria2.models import Aria2


@admin.register(Aria2)
class Aria2Admin(admin.ModelAdmin):
    """
    The admin of Aria2 model of aria2
    """
