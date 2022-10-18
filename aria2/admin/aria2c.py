"""
The admin of Aria2 model of aria2
"""
import subprocess

from django.contrib import admin

from aria2.models import Aria2c


@admin.register(Aria2c)
class Aria2Admin(admin.ModelAdmin):
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
