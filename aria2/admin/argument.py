"""
The admin of Aria2 Argument and Aria2 Argument Tag model of aria2
"""
import logging

from django.contrib import admin

from ..models import Argument, ArgumentTag
from .utils import ReadOnlyAdminMixin

logger = logging.getLogger(__name__)


@admin.register(ArgumentTag)
class Aria2cArgumentTagAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Argument Tag model of aria2
    """

    list_display = ("value", "number_of_arguments")
    ordering = ("value",)
    readonly_fields = ("number_of_arguments",)

    @admin.display()
    def number_of_arguments(self, obj: ArgumentTag) -> int:
        """

        :param obj:
        :type obj: ArgumentTag
        :return:
        :rtype: int
        """
        return obj.argument_set.count()


@admin.register(Argument)
class Aria2cArgumentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 Argument model of aria2
    """

    list_display = (
        "long_argument",
        "short_argument",
        "default",
        "description",
        "possible_values",
        "binary",
    )
    ordering = ("long_argument",)
    search_fields = ("short_argument", "long_argument", "description")
