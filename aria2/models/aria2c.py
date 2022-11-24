"""
The model of Aria2
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Optional, TypeVar

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Col

from ..exceptions import CommandNotFound

_T = TypeVar("_T", bound=BaseDatabaseWrapper)

logger = logging.getLogger(__name__)


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


Manager = models.Manager.from_queryset(QuerySet)


class Aria2c(models.Model):
    """
    The model of Aria2
    """

    path = PathField(max_length=256)

    objects = Manager()

    class Meta:
        verbose_name = "Aria2c - Binary"
        verbose_name_plural = "Aria2c - Binaries"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return str(self.path)

    def get_pids(self) -> tuple[int, ...]:
        """

        :return:
        :rtype: tuple[int, ...]
        """
        try:
            return tuple(
                int(pid)
                for pid in subprocess.check_output(["pidof", str(self.path)])
                .decode()
                .split()
            )
        except subprocess.CalledProcessError:
            return tuple()

    @staticmethod
    def get_command(pid: int | str) -> str:
        """

        :param pid:
        :type pid: int
        :return:
        :rtype: int | str
        """
        return (
            subprocess.check_output(
                ["ps", "-p", str(pid), "-o", "args", "--no-headers"]
            )
            .decode()
            .strip()
        )

    def get_pid(self, command: str) -> int:
        """

        :param command:
        :type command: str
        :return:
        :rtype: int
        """
        for pid in self.get_pids():
            if command == self.get_command(pid):
                return pid
        raise CommandNotFound
