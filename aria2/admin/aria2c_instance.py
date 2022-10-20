"""
The admin of Aria2 Instance model of aria2
"""
import subprocess
from datetime import timedelta

from django.contrib import admin

from ..models import Aria2cInstance
from .utils import ReadOnlyAdminMixin


@admin.register(Aria2cInstance)
class Aria2cInstanceAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Instance model of aria2
    """

    list_display = ("pid", "command", "running", "aria2c")
    readonly_fields = ("running",)

    @admin.display()
    def running(self, obj: Aria2cInstance) -> timedelta:
        """
        get the running time of the Aria2 Instance
        :param obj:
        :return:
        """
        return timedelta(
            seconds=int(
                subprocess.check_output(
                    ["ps", "-p", str(obj.pid), "-o", "etimes", "--no-headers"]
                ).decode()
            )
        )
