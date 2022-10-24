"""
The model of Aria2 Instance
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import models

from ..exceptions import CommandExecutionFailed, CommandNotFound

if TYPE_CHECKING:
    from .aria2c import Aria2c as TAria2c
    from .aria2c_profile import Aria2cProfile as TAria2cProfile


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit aria2c
    """

    def create_from_pid(self, pid: int | str) -> Aria2cInstance:
        """

        :param pid:
        :type pid: int | str
        :return:
        :rtype: Aria2cInstance
        """
        Aria2c: TAria2c = apps.get_model(app_label="aria2", model_name="Aria2c")
        command = Aria2c.get_command(pid)
        aria2c, _ = Aria2c.objects.get_or_create(path=command.split(maxsplit=1)[0])
        return self.create(pid=pid, command=command, aria2c=aria2c)

    def create_all_from_aria2c(self, aria2c: TAria2c) -> tuple[Aria2cInstance, ...]:
        """

        :param aria2c:
        :type aria2c: TAria2c
        :return:
        :rtype: tuple[Aria2cInstance, ...]
        """
        return tuple(
            self.create(pid=pid, command=aria2c.get_command(pid), aria2c=aria2c)
            for pid in aria2c.get_pids()
        )

    def create_from_profile(self, profile: TAria2cProfile) -> Aria2cInstance:
        """

        :param profile:
        :type profile: TAria2cProfile
        :return:
        :rtype: Aria2cInstance
        """
        command = " ".join(profile.command)
        try:
            return self.get(command=command)
        except Aria2cInstance.DoesNotExist:
            with subprocess.Popen(profile.command):
                start = datetime.now()
                while True:
                    try:
                        pid = profile.aria2c.get_pid(command)
                    except CommandNotFound as exc:
                        if (datetime.now() - start) > timedelta(seconds=30):
                            raise CommandExecutionFailed from exc
                        continue
                    return self.create(pid=pid, command=command, aria2c=profile.aria2c)


Manager = models.Manager.from_queryset(QuerySet)


class Aria2cInstance(models.Model):
    """
    The model of Aria2 instance
    """

    pid = models.IntegerField(primary_key=True)
    command = models.CharField(max_length=256, unique=True)

    aria2c = models.ForeignKey("Aria2c", on_delete=models.CASCADE)

    objects = Manager()

    class Meta:
        verbose_name = "Aria2c - Instance"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return str(self.pid)
