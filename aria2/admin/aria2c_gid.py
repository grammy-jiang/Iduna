"""
The admin of Aria2 GID model of aria2
"""
from typing import Optional, TypeVar

from django.contrib import admin
from django.http import HttpRequest as _HttpRequest
from django.http import HttpResponse

from ..models import Aria2cGID, Aria2cGIDMetaLink, Aria2cGIDTorrent, Aria2cGIDUri

HttpRequest = TypeVar("HttpRequest", bound=_HttpRequest)


@admin.register(Aria2cGID)
class Aria2cGIDAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID model of aria2
    """

    fields = (
        "gid",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
        "verbose_status",
        "instance",
        "updated_at",
        "created_at",
    )
    list_display = (
        "gid",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
        "updated_at",
        "created_at",
    )
    readonly_fields = (
        "gid",
        "status",
        "completed_percentage",
        "completed_length",
        "total_length",
        "dir",
        "verbose_status",
        "created_at",
        "updated_at",
    )

    @admin.display()
    def completed_percentage(self, obj: Aria2cGID) -> Optional[float]:
        """

        :param obj:
        :type obj: Aria2cGID
        :return:
        :rtype: Optional[float]
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


@admin.register(Aria2cGIDUri)
class Aria2cGIDUriAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID Uri model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "uris", "options", "position")
    readonly_fields = ("gid",)

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Aria2cGIDUri] = None
    ) -> bool:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Optional[Aria2cGIDUri]
        :return:
        :rtype: bool
        """
        return False

    def response_change(self, request: HttpRequest, obj: Aria2cGIDUri) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Aria2cGIDUri
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)


@admin.register(Aria2cGIDTorrent)
class Aria2cGIDTorrentAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID Torrent model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "torrent", "uris", "options", "position")
    readonly_fields = ("gid",)

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Aria2cGIDUri] = None
    ) -> bool:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Optional[Aria2cGIDUri]
        :return:
        :rtype: bool
        """
        return False

    def response_change(
        self, request: HttpRequest, obj: Aria2cGIDTorrent
    ) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Aria2cGIDTorrent
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)


@admin.register(Aria2cGIDMetaLink)
class Aria2cGIDMetaLinkAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID MetaLink model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "metalink", "options", "position")
    readonly_fields = ("gid",)

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[Aria2cGIDUri] = None
    ) -> bool:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Optional[Aria2cGIDUri]
        :return:
        :rtype: bool
        """
        return False

    def response_change(
        self, request: HttpRequest, obj: Aria2cGIDMetaLink
    ) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Aria2cGIDMetaLink
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)
