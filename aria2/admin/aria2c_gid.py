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
        "status",
        "verbose_status",
        "total_length",
        "completed_length",
        "dir",
        "completed_percentage",
    )
    list_display = (
        "gid",
        "uris",
        "status",
        "total_length",
        "completed_length",
        "dir",
        "completed_percentage",
    )
    # readonly_fields = (
    #     "gid",
    #     "uris",
    #     "status",
    #     "verbose_status",
    #     "total_length",
    #     "completed_length",
    #     "dir",
    #     "completed_percentage",
    # )

    @admin.display()
    def completed_percentage(self, obj: Aria2cGID) -> float:
        """

        :param obj:
        :type obj: Aria2cGID
        :return:
        :rtype: float
        """
        return round(int(obj.completed_length) / int(obj.total_length), 2)

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
