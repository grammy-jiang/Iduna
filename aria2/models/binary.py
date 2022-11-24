"""
The model of Aria2
"""
from __future__ import annotations

import logging
import pprint
import subprocess
from pathlib import Path
from typing import Optional, TypeVar

from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.expressions import Col

from ..exceptions import CommandNotFound

_T = TypeVar("_T", bound=BaseDatabaseWrapper)

logger = logging.getLogger("django")


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

    def create_from_file_system(self) -> QuerySet:
        """

        :return:
        :rtype: QuerySet
        """
        paths = set(
            subprocess.check_output(["which", "--all", "aria2c"])
            .decode()
            .strip()
            .split("\n")
        )
        paths_in_database = set(
            str(path) for path in self.values_list("path", flat=True)
        )

        self.filter(path__in=paths_in_database.difference(paths))
        logger.info(
            "The paths existed in the database but not in $PATH are removed:\n%s",
            pprint.pformat(sorted(list(paths_in_database.difference(paths)))),
        )

        for path in paths.difference(paths_in_database):
            self.create(path=path)
        logger.info(
            "The paths existed in $PATH but not in the database are created:\n%s",
            pprint.pformat(sorted(list(paths.difference(paths_in_database)))),
        )

        return self.all()


Manager = models.Manager.from_queryset(QuerySet)


class Binary(models.Model):
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
