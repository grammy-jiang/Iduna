"""
The admin of Aria2 GID model of aria2
"""
from typing import Optional, TypeVar

from django.contrib import admin
from django.http import HttpRequest as _HttpRequest

from ..models import Aria2cGID

HttpRequest = TypeVar("HttpRequest", bound=_HttpRequest)


@admin.register(Aria2cGID)
class Aria2cGIDAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID model of aria2
    """

    fields = (
        "gid",
        "uris",
        "options",
        "position",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
        "verbose_status",
        "instance",
    )
    list_display = (
        "gid",
        "uris",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
    )
    readonly_fields = (
        "gid",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
        "verbose_status",
        "instance",
    )

    @admin.display()
    def completed_percentage(self, obj: Aria2cGID) -> float:
        """

        :param obj:
        :type obj: Aria2cGID
        :return:
        :rtype: float
        """
        try:
            return round(int(obj.completed_length) / int(obj.total_length), 2)
        except ZeroDivisionError:
            return None

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Aria2cGID] = None
    ) -> bool:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Optional[Aria2cGID]
        :return:
        :rtype: bool
        """
        return False
