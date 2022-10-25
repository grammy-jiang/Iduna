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

    @admin.display(description="Effective User Name")
    @safe_check_output
    def effective_user_name(self, obj: Aria2cInstance) -> str:
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

    @admin.display(description="Elapsed Time")
    @safe_check_output
    def elapsed_time(self, obj: Aria2cInstance) -> timedelta:
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

    @admin.display(description="Cumulative CPU Time")
    @safe_check_output
    def cumulative_cpu_times(self, obj: Aria2cInstance) -> timedelta:
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
        "effective_user_name",
        "cpu",
        "mem",
        "elapsed_time",
        "cumulative_cpu_times",
        "aria2c",
        "verbose_version",
        "session_id",
        "global_statistics",
        "available_methods",
        "available_notifications",
        "global_options",
    )
    list_display = (
        "profile",
        "pid",
        "command",
        "effective_user_name",
        "cpu",
        "mem",
        "elapsed_time",
        "cumulative_cpu_times",
        "aria2c",
        "version",
    )
    readonly_fields = (
        "effective_user_name",
        "mem",
        "elapsed_time",
        "cumulative_cpu_times",
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
    def session_id(self, obj: Aria2cInstance) -> str:
        """

        :param obj:
        :type obj: Aria2cInstance
        :return:
        :rtype: str
        """
        return obj.rpc_server_proxy.aria2.getSessionInfo()["sessionId"]

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
