"""
The model of Aria2
"""
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


class Aria2c(models.Model):
    """
    The model of Aria2
    """

    path = PathField(max_length=256, primary_key=True)

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
