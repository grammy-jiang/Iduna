"""
The model of Aria2
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional, TypeVar

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Col

_T = TypeVar("_T", bound=BaseDatabaseWrapper)


class PathField(models.CharField):
    """
    custom field to convert str to pathlib.Path
    """

    def from_db_value(
        self, value: Optional[str], expression: Col, connection: _T
    ) -> Optional[Path]:
        """
        If present for the field subclass, from_db_value() will be called in all
        circumstances when the data is loaded from the database, including in aggregates
        and values() calls.
        :param value:
        :type value: Optional[str]
        :param expression:
        :param expression: Col
        :param connection:
        :type connection: _T
        :return:
        :type: Optional[Path]
        """
        if value is None:
            return value
        return Path(value)


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit the local file system
    """

    def create_from_file_system(self) -> list[Aria2c]:
        """

        :return:
        :rtype: list[Aria2c]
        """
        aria2cs: list[Aria2c] = []
        for path in (
            subprocess.check_output(["which", "--all", "aria2c"])
            .decode()
            .strip()
            .split("\n")
        ):
            aria2cs.append(self.create(path=path))
        return aria2cs


class Manager(models.Manager):
    """
    custom Manager to fit the local file system
    """


class Aria2c(models.Model):
    """
    The model of Aria2
    """

    path = PathField(max_length=256, primary_key=True)

    objects = Manager.from_queryset(QuerySet)()

    class Meta:
        verbose_name = "Aria2c - Binary"
        verbose_name_plural = "Aria2c - Binaries"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return str(self.path)

    def _get_pids(self) -> tuple[int, ...]:
        """

        :return:
        :rtype: tuple[int, ...]
        """
        return tuple(
            int(pid)
            for pid in subprocess.check_output(["pidof", self.path]).decode().split()
        )

    def _get_command(self, pid: int) -> str:
        """

        :param pid:
        :type pid: int
        :return:
        :rtype: str
        """
        return subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "args", "--no-headers"]
        ).decode()
