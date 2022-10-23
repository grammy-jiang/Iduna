"""
The model of Aria2 Instance
"""
from __future__ import annotations

from django.db import models

from .aria2c import Aria2c


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
        command = Aria2c.get_command(pid)
        aria2c, _ = Aria2c.objects.get_or_create(path=command.split(maxsplit=1)[0])
        return self.create(pid=pid, command=command, aria2c=aria2c)

    def create_all_from_aria2c(self, aria2c: Aria2c) -> tuple[Aria2cInstance, ...]:
        """

        :param aria2c:
        :type aria2c: Aria2c
        :return:
        :rtype: tuple[Aria2cInstance, ...]
        """
        return tuple(
            self.create(pid=pid, command=aria2c.get_command(pid), aria2c=aria2c)
            for pid in aria2c.get_pids()
        )


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
