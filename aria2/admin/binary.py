"""
The admin of Aria2 model of aria2
"""
import logging
import subprocess

from django.contrib import admin

from ..models import Aria2cInstance, Binary
from .instance import Aria2cInstanceMixin
from .profile import Profile
from .utils import ReadOnlyAdminMixin

logger = logging.getLogger(__name__)


class Aria2cInstanceInline(Aria2cInstanceMixin, admin.TabularInline):
    """
    The tabular inline of Aria2 Instance
    """

    fields = (
        "pid",
        "command",
        "effective_user_name",
        "cpu",
        "mem",
        "elapsed_time",
        "cumulative_cpu_times",
    )
    readonly_fields = (
        "pid",
        "command",
        "effective_user_name",
        "cpu",
        "mem",
        "elapsed_time",
        "cumulative_cpu_times",
    )
    model = Aria2cInstance


class Aria2cProfileInline(admin.TabularInline):
    """
    The tabular inline of Aria2 Profile Instance
    """

    fields = ("name", "args")
    model = Profile
    readonly_fields = ("args",)

    @admin.display()
    def args(self, obj: Profile) -> str:
        """

        :param obj:
        :type obj: Profile
        :return:
        :rtype: str
        """
        return ", ".join(obj.args)


@admin.register(Binary)
class Aria2cAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    """
    The admin of Aria2 model of aria2
    """

    fields = ("path", "verbose_version")
    inlines = (Aria2cInstanceInline, Aria2cProfileInline)
    list_display = ("path", "version", "instances")
    readonly_fields = ("path", "version", "verbose_version", "instances")

    @admin.display()
    def version(self, obj: Binary) -> str:
        """

        :param obj:
        :type obj: Binary
        :return:
        :rtype: str
        """
        return (
            subprocess.check_output([obj.path, "--version"])
            .decode()
            .split("\n", maxsplit=1)[0]
            .replace("aria2 version ", "")
        )

    @admin.display()
    def verbose_version(self, obj: Binary) -> str:
        """

        :param obj:
        :type obj: Binary
        :return:
        :rtype: str
        """
        return subprocess.check_output([obj.path, "--version"]).decode()

    @admin.display()
    def instances(self, obj: Binary) -> str:
        """

        :param obj:
        :type obj: Binary
        :return:
        :rtype: str
        """
        return ", ".join(
            str(instance.pid) for instance in Aria2cInstance.objects.filter(aria2c=obj)
        )
