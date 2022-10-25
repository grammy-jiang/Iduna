"""
The admin of Aria2 model of aria2
"""
import subprocess

from django.contrib import admin

from ..models import Aria2c, Aria2cInstance
from .aria2c_instance import Aria2cInstanceMixin
from .aria2c_profile import Aria2cProfile
from .utils import ReadOnlyAdminMixin


class Aria2cInstanceInline(Aria2cInstanceMixin, admin.TabularInline):
    """
    The tabular inline of Aria2 Instance
    """

    fields = ("pid", "command", "euser", "cpu", "mem", "etimes", "cputimes")
    readonly_fields = ("pid", "command", "euser", "cpu", "mem", "etimes", "cputimes")
    model = Aria2cInstance


class Aria2cProfileInline(admin.TabularInline):
    """
    The tabular inline of Aria2 Profile Instance
    """

    fields = ("name", "args")
    model = Aria2cProfile
    readonly_fields = ("args",)

    @admin.display()
    def args(self, obj: Aria2cProfile) -> str:
        """

        :param obj:
        :type obj: Aria2cProfile
        :return:
        :rtype: str
        """
        return ", ".join(obj.args)


@admin.register(Aria2c)
class Aria2cAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 model of aria2
    """

    fields = ("path", "verbose_version")
    inlines = (Aria2cInstanceInline, Aria2cProfileInline)
    list_display = ("path", "version")
    readonly_fields = ("path", "version", "verbose_version")

    @admin.display()
    def version(self, obj: Aria2c) -> str:
        """

        :param obj:
        :type obj: Aria2c
        :return:
        :rtype: str
        """
        return (
            subprocess.check_output([obj.path, "--version"])
            .decode()
            .split("\n", maxsplit=1)[0]
            .replace("aria2 version ", "")
        )

    @admin.display()
    def verbose_version(self, obj: Aria2c) -> str:
        """

        :param obj:
        :type obj: Aria2c
        :return:
        :rtype: str
        """
        return subprocess.check_output([obj.path, "--version"]).decode()
