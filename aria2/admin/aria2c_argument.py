"""
The admin of Aria2 Argument and Aria2 Argument Tag model of aria2
"""

from django.contrib import admin

from ..models import Aria2cArgument, Aria2cArgumentTag
from .utils import ReadOnlyAdminMixin


class Aria2cArgumentInline(admin.TabularInline):
    """
    the inline of Aria2 Argument model
    """

    model = Aria2cArgument.tags.through


@admin.register(Aria2cArgumentTag)
class Aria2cArgumentTagAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Argument Tag model of aria2
    """

    inlines = (Aria2cArgumentInline,)

    list_display = ("value",)
    ordering = ("value",)


@admin.register(Aria2cArgument)
class Aria2cArgumentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Argument model of aria2
    """

    list_display = (
        "short_argument",
        "long_argument",
        "description",
        "default",
        "possible_values",
        "aria2c",
    )
    ordering = ("long_argument",)
    search_fields = ("short_argument", "long_argument", "description")
