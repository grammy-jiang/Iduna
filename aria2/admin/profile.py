"""
The admin of Aria2 Profile model of aria2
"""
import logging
from typing import TypeVar

from django.contrib import admin
from django.http import HttpRequest as _HttpRequest
from django.http import HttpResponse

from ..models import ArgumentPair, Instance, Profile

HttpRequest = TypeVar("HttpRequest", bound=_HttpRequest)

logger = logging.getLogger(__name__)


@admin.register(ArgumentPair)
class ArgumentPairAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 Argument Pair model of aria2
    """

    list_display = ("profile", "argument", "value")
    ordering = ("profile", "argument")


class ArgumentPairInline(admin.TabularInline):
    """
    The inline of Argument Pair
    """

    model = ArgumentPair
    ordering = ("argument",)


class Aria2cInstanceInline(admin.TabularInline):
    """
    The inline of Aria2 Instance
    """

    exclude = ("verbose_version",)
    model = Instance
    readonly_fields = (
        "pid",
        "command",
        "binary",
        "effective_user_name",
        "version",
        "session_id",
    )


@admin.register(Profile)
class Aria2cProfileAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 Profile model of aria2
    """

    change_form_template = "aria2/admin/change_form_profile.html"
    fields = ("name", "binary")
    inlines = (ArgumentPairInline, Aria2cInstanceInline)
    list_display = ("name", "binary", "args")

    def response_change(self, request: HttpRequest, obj: Profile) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Profile
        :return:
        :rtype: HttpResponse
        """
        if "_create-instance" in request.POST:
            Instance.objects.create_from_profile(obj)
        return super().response_change(request, obj)
