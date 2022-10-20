"""
The admin of Aria2 model of aria2
"""
import subprocess

from django.contrib import admin

from ..models import Aria2c, Aria2cInstance
from .aria2c_instance import Aria2cInstanceMixin
from .utils import ReadOnlyAdminMixin


class Aria2cInstanceInline(Aria2cInstanceMixin, admin.TabularInline):
    """
    The tabular inline of Aria2 Instance
    """

    fields = ("pid", "command", "euser", "cpu", "mem", "etimes", "cputimes")
    readonly_fields = ("euser", "cpu", "mem", "etimes", "cputimes")
    model = Aria2cInstance


@admin.register(Aria2c)
class Aria2cAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 model of aria2
    """

    inlines = [
        Aria2cInstanceInline,
    ]

    fields = ("path", "version")
    list_display = ("path",)
    readonly_fields = ("version",)

    @admin.display()
    def version(self, obj: Aria2c) -> str:
        """

        :param obj:
        :type obj: Aria2c
        :return:
        :rtype: str
        """
        return subprocess.check_output([obj.path, "--version"]).decode()
