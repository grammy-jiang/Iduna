"""
The admin of Aria2 model of aria2
"""
import subprocess

from django.contrib import admin

from ..models import Aria2c
from .utils import ReadOnlyAdminMixin


@admin.register(Aria2c)
class Aria2Admin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 model of aria2
    """

    fields = ("path", "version")
    list_display = ("path",)
    readonly_fields = ("version",)

    @admin.display()
    def version(self, obj: Aria2c) -> str:
        """

        :param obj:
        :type obj: Aria2c
        :return:
        :rtype: str
        """
        return subprocess.check_output([obj.path, "--version"]).decode()
