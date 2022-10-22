"""
The model of Aria2 Instance
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from .aria2c import Aria2c


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit aria2c
    """

    def create_all_from_aria2c(self, aria2c: Aria2c) -> tuple[Aria2cInstance, ...]:
        """

        :param aria2c:
        :type aria2c: Aria2c
        :return:
        :rtype: tuple[Aria2cInstance, ...]
        """
        return tuple(
            self.create(pid=pid, command=aria2c._get_command(pid), aria2c=aria2c)
            for pid in aria2c._get_pids()
        )


class Manager(models.Manager):
    """
    custom Manager to fit aria2c
    """


class Aria2cInstance(models.Model):
    """
    The model of Aria2 instance
    """

    pid = models.IntegerField(primary_key=True)
    command = models.CharField(db_index=True, max_length=256)

    aria2c = models.ForeignKey("Aria2c", on_delete=models.CASCADE)

    objects = Manager.from_queryset(QuerySet)()

    class Meta:
        verbose_name = "Aria2c - Instance"
