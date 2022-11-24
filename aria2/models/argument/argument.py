"""
The model of Aria2 Argument and Argument Tag
"""
from __future__ import annotations

import logging
import re
import subprocess
from typing import TYPE_CHECKING

from django.apps import apps
from django.db import models

if TYPE_CHECKING:
    from ..binary import Binary
    from .tag import ArgumentTag as TAria2cArgumentTag

logger = logging.getLogger(__name__)

beginning_regex = re.compile(
    r"""
        ^\s
        ((?P<short_argument>-\S+?)(,\s)?)?
        (?P<long_argument>--\S+?)
        (\[?=\S+?]?)?
        \s+
        (?P<description>.+)$
    """,
    re.VERBOSE,
)
category_regex = re.compile(
    r"""
        ^\s{30}
        (?P<key>(Possible\sValues)|(Default)|(Tags)):\s
        (?P<value>.+)
    """,
    re.VERBOSE,
)


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit Aria2 Argument
    """

    def create_from_binary(self, binary: Binary) -> QuerySet:
        """

        :param binary:
        :type binary: Binary
        :return:
        :rtype: QuerySet
        """
        self.filter(binary=binary).delete()

        ArgumentTag: TAria2cArgumentTag = apps.get_model("aria2", "ArgumentTag")

        argument: Argument = None
        line: str
        for line in filter(
            None,
            subprocess.check_output([binary.path, "--help=#all"])
            .decode()
            .split("\n")[3:-3],
        ):
            if m := beginning_regex.match(line):
                if argument:
                    argument.save()
                argument = self.create(binary=binary, **m.groupdict())
                continue
            if m := category_regex.match(line):
                key, value = m.groupdict()["key"], m.groupdict()["value"]
                if key != "Tags":
                    setattr(
                        argument,
                        key.lower().replace(" ", "_"),
                        value.replace("#", ""),
                    )
                    continue
                for i in value.split(", "):  # tags
                    argument.tags.add(ArgumentTag.objects.get_or_create(value=i)[0])
                continue
            argument.description = " ".join((argument.description, line.strip()))
        argument.save()
        return self.filter(binary=binary)


Manager = models.Manager.from_queryset(QuerySet)


class Argument(models.Model):
    """
    the model of Aria2 Argument
    """

    short_argument = models.CharField(
        blank=True, max_length=256, null=True, unique=True
    )
    long_argument = models.CharField(max_length=256, primary_key=True)
    description = models.CharField(max_length=256)
    possible_values = models.CharField(blank=True, max_length=256, null=True)
    default = models.CharField(blank=True, max_length=256, null=True)
    tags = models.ManyToManyField("ArgumentTag")

    binary = models.ForeignKey("Binary", on_delete=models.CASCADE)

    objects = Manager()

    class Meta:
        verbose_name = "Aria2c - Argument"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self.long_argument
