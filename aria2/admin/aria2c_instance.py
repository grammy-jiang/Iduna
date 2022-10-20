"""
The admin of Aria2 Instance model of aria2
"""
import subprocess
from datetime import timedelta

from django.contrib import admin

from ..models import Aria2cInstance
from .utils import ReadOnlyAdminMixin


class Aria2cInstanceMixin:
    """
    The mixin for the admin of Aria2 Instance
    """

    @admin.display()
    def euser(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return subprocess.check_output(
            ["ps", "-p", str(obj.pid), "-o", "euser", "--no-headers"]
        ).decode()

    @admin.display()
    def mem(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return subprocess.check_output(
            ["ps", "-p", str(obj.pid), "-o", "%mem", "--no-headers"]
        ).decode()

    @admin.display()
    def etimes(self, obj: Aria2cInstance) -> timedelta:
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

    @admin.display()
    def cpu(self, obj: Aria2cInstance) -> float:
        """

        :param obj:
        :type obj:
        :return:
        :rtype: float
        """
        return float(
            subprocess.check_output(
                ["ps", "-p", str(obj.pid), "-o", "%cpu", "--no-headers"]
            ).decode()
        )

    @admin.display()
    def cputimes(self, obj: Aria2cInstance) -> timedelta:
        """

        :param obj:
        :type obj:
        :return:
        :rtype: timedelta
        """
        return timedelta(
            seconds=int(
                subprocess.check_output(
                    ["ps", "-p", str(obj.pid), "-o", "cputimes", "--no-headers"]
                ).decode()
            )
        )


@admin.register(Aria2cInstance)
class Aria2cInstanceAdmin(ReadOnlyAdminMixin, Aria2cInstanceMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Instance model of aria2
    """

    list_display = (
        "pid",
        "command",
        "euser",
        "cpu",
        "mem",
        "etimes",
        "cputimes",
        "aria2c",
    )
    readonly_fields = ("euser", "mem", "etimes", "cputimes", "cpu")
