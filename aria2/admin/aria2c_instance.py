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
        "session_id",
        "global_statistics",
        "available_methods",
        "available_notifications",
        "global_options",
    )
