"""
The admin of Aria2 Instance model of aria2
"""
import logging
import pprint
from typing import Optional

from django.contrib import admin
from django.utils.html import format_html

from ..models import GID, Instance
from .utils import ReadOnlyAdminMixin

logger = logging.getLogger(__name__)


class Aria2cInstanceMixin:
    """
    The mixin for the admin of Aria2 Instance
    """

    @admin.display()
    def verbose_version(self, obj: Instance) -> Optional[str]:
        """

        :param obj:
        :type obj: Instance
        :return:
        :rtype: Optional[str]
        """
        try:
            return format_html(
                "<pre>{}</pre>",
                pprint.pformat(obj.rpc_server_proxy.aria2.getVersion()),
            )
        except ConnectionRefusedError as exc:
            logger.exception(exc)

    @admin.display()
    def global_statistics(self, obj: Instance) -> Optional[str]:
        """

        :param obj:
        :type obj: Instance
        :return:
        :rtype: Optional[str]
        """
        try:
            return format_html(
                "<pre>{}</pre>",
                pprint.pformat(obj.rpc_server_proxy.aria2.getGlobalStat()),
            )
        except ConnectionRefusedError as exc:
            logger.exception(exc)

    @admin.display()
    def available_methods(self, obj: Instance) -> Optional[str]:
        """

        :param obj:
        :type obj: Instance
        :return:
        :rtype: Optional[str]
        """
        try:
            return format_html(
                "<pre>{}</pre>",
                pprint.pformat(obj.rpc_server_proxy.system.listMethods()),
            )
        except ConnectionRefusedError as exc:
            logger.exception(exc)

    @admin.display()
    def available_notifications(self, obj: Instance) -> Optional[str]:
        """

        :param obj:
        :type obj: Instance
        :return:
        :rtype: Optional[str]
        """
        try:
            return format_html(
                "<pre>{}</pre>",
                pprint.pformat(obj.rpc_server_proxy.system.listNotifications()),
            )
        except ConnectionRefusedError as exc:
            logger.exception(exc)

    @admin.display()
    def global_options(self, obj: Instance) -> Optional[str]:
        """

        :param obj:
        :type obj: Instance
        :return:
        :rtype: Optional[str]
        """
        try:
            return format_html(
                "<pre>{}</pre>",
                pprint.pformat(obj.rpc_server_proxy.aria2.getGlobalOption()),
            )
        except ConnectionRefusedError as exc:
            logger.exception(exc)


class Aria2cGIDInline(admin.TabularInline):
    """
    the inline of Aria2cGID
    """

    model = GID


@admin.register(Instance)
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
    inlines = (Aria2cGIDInline,)
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

    def has_delete_permission(self, request, obj=None) -> bool:
        """

        :param request:
        :type request:
        :param obj:
        :type obj:
        :return:
        :rtype: bool
        """
        return True
