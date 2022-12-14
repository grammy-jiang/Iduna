"""
The admin of Aria2 GID model of aria2
"""
import logging
from typing import Optional, TypeVar

from django.contrib import admin
from django.http import HttpRequest as _HttpRequest
from django.http import HttpResponse

from ..models import GID, GIDMetaLink, GIDTorrent, GIDUri

HttpRequest = TypeVar("HttpRequest", bound=_HttpRequest)

logger = logging.getLogger(__name__)


@admin.register(GID)
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
    def completed_percentage(self, obj: GID) -> Optional[float]:
        """

        :param obj:
        :type obj: GID
        :return:
        :rtype: Optional[float]
        """
        try:
            return round(int(obj.completed_length) / int(obj.total_length), 2)
        except ZeroDivisionError:
            return None

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[GID] = None
    ) -> bool:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Optional[GID]
        :return:
        :rtype: bool
        """
        return False


@admin.register(GIDUri)
class Aria2cGIDUriAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID Uri model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "uris", "options", "position")
    readonly_fields = ("gid",)

    def response_change(self, request: HttpRequest, obj: GIDUri) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: GIDUri
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)


@admin.register(GIDTorrent)
class Aria2cGIDTorrentAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID Torrent model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "torrent", "uris", "options", "position")
    readonly_fields = ("gid",)

    def response_change(self, request: HttpRequest, obj: GIDTorrent) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: GIDTorrent
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)


@admin.register(GIDMetaLink)
class Aria2cGIDMetaLinkAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 GID MetaLink model of aria2
    """

    change_form_template = "aria2/admin/change_form_gid.html"
    list_display = ("gid", "metalink", "options", "position")
    readonly_fields = ("gid",)

    def response_change(self, request: HttpRequest, obj: GIDMetaLink) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: GIDMetaLink
        :return:
        :rtype: HttpResponse
        """
        if "_create-gid" in request.POST and not obj.gid:
            obj.create_gid()
        return super().response_change(request, obj)
