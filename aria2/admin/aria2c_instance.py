"""
The admin of Aria2 Instance model of aria2
"""
import pprint
import subprocess
from datetime import timedelta

from django.contrib import admin

from ..models import Aria2cInstance
from .utils import ReadOnlyAdminMixin, safe_check_output


class Aria2cInstanceMixin:
    """
    The mixin for the admin of Aria2 Instance
    """

    @admin.display()
    @safe_check_output
    def euser(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return (
            subprocess.check_output(
                ["ps", "-p", str(obj.pid), "-o", "euser", "--no-headers"]
            )
            .decode()
            .strip()
        )

    @admin.display()
    @safe_check_output
    def mem(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return (
            subprocess.check_output(
                ["ps", "-p", str(obj.pid), "-o", "%mem", "--no-headers"]
            )
            .decode()
            .strip()
        )

    @admin.display()
    @safe_check_output
    def etimes(self, obj: Aria2cInstance) -> timedelta:
        """
        get the running time of the Aria2 Instance
        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: timedelta
        """
        return timedelta(
            seconds=int(
                subprocess.check_output(
                    ["ps", "-p", str(obj.pid), "-o", "etimes", "--no-headers"]
                )
                .decode()
                .strip()
            )
        )

    @admin.display()
    @safe_check_output
    def cpu(self, obj: Aria2cInstance) -> float:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: float
        """
        return float(
            subprocess.check_output(
                ["ps", "-p", str(obj.pid), "-o", "%cpu", "--no-headers"]
            )
            .decode()
            .strip()
        )

    @admin.display()
    @safe_check_output
    def cputimes(self, obj: Aria2cInstance) -> timedelta:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: timedelta
        """
        return timedelta(
            seconds=int(
                subprocess.check_output(
                    ["ps", "-p", str(obj.pid), "-o", "cputimes", "--no-headers"]
                )
                .decode()
                .strip()
            )
        )


@admin.register(Aria2cInstance)
class Aria2cInstanceAdmin(ReadOnlyAdminMixin, Aria2cInstanceMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Instance model of aria2
    """

    fields = (
        "profile",
        "pid",
        "command",
        "euser",
        "cpu",
        "mem",
        "etimes",
        "cputimes",
        "aria2c",
        "verbose_version",
        "available_methods",
        "available_notifications",
        "global_options",
        "global_statistics",
        "session_id",
    )
    list_display = (
        "profile",
        "pid",
        "command",
        "euser",
        "cpu",
        "mem",
        "etimes",
        "cputimes",
        "aria2c",
        "version",
    )
    readonly_fields = (
        "euser",
        "mem",
        "etimes",
        "cputimes",
        "cpu",
        "version",
        "verbose_version",
        "available_methods",
        "available_notifications",
        "global_options",
        "global_statistics",
        "session_id",
    )

    @admin.display()
    def version(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return obj.rpc_server_proxy.aria2.getVersion()["version"]

    @admin.display()
    def verbose_version(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return pprint.pformat(obj.rpc_server_proxy.aria2.getVersion())

    @admin.display()
    def available_methods(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return pprint.pformat(obj.rpc_server_proxy.system.listMethods())

    @admin.display()
    def available_notifications(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return pprint.pformat(obj.rpc_server_proxy.system.listNotifications())

    @admin.display()
    def global_options(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return pprint.pformat(obj.rpc_server_proxy.aria2.getGlobalOption())

    @admin.display()
    def global_statistics(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return pprint.pformat(obj.rpc_server_proxy.aria2.getGlobalStat())

    @admin.display()
    def session_id(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return obj.rpc_server_proxy.aria2.getSessionInfo()["sessionId"]
