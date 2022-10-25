"""
The admin of Aria2 Profile model of aria2
"""

from typing import TypeVar

from django.contrib import admin
from django.http import HttpRequest as _HttpRequest
from django.http import HttpResponse

from ..models import ArgumentPair, Aria2cInstance, Aria2cProfile

HttpRequest = TypeVar("HttpRequest", bound=_HttpRequest)


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

    model = Aria2cInstance
    readonly_fields = ("pid", "command", "aria2c")


@admin.register(Aria2cProfile)
class Aria2cProfileAdmin(admin.ModelAdmin):
    """
    The admin of Aria2 Profile model of aria2
    """

    change_form_template = "aria2/admin/change_form_profile.html"
    fields = ("name", "aria2c")
    inlines = (ArgumentPairInline, Aria2cInstanceInline)
    list_display = ("name", "aria2c", "args")

    def response_change(self, request: HttpRequest, obj: Aria2cProfile) -> HttpResponse:
        """

        :param request:
        :type request: HttpRequest
        :param obj:
        :type obj: Aria2cProfile
        :return:
        :rtype: HttpResponse
        """
        if "_create-instance" in request.POST:
            Aria2cInstance.objects.create_from_profile(obj)
        return super().response_change(request, obj)
