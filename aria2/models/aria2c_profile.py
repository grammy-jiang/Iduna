"""
The model of Aria2 Profile
"""
from __future__ import annotations

import logging
from typing import Iterable, Optional

from django.db import models
from django.utils.functional import cached_property

logger = logging.getLogger(__name__)


class Aria2cProfile(models.Model):
    """
    The model of Aria2 Profile
    """

    name = models.CharField(max_length=256, primary_key=True)
    aria2c = models.ForeignKey("Binary", on_delete=models.CASCADE)

    arguments = models.ManyToManyField("Argument", through="ArgumentPair")

    args = models.CharField(blank=True, max_length=256, null=True, unique=True)

    class Meta:
        verbose_name = "Aria2c - Profile"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self.name

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        """

        :param force_insert:
        :type force_insert: bool
        :param force_update:
        :type force_update: bool
        :param using:
        :type using: Optional[str]
        :param update_fields:
        :type update_fields: Optional[Iterable[str]]
        :return:
        :rtype: None
        """
        self.args = " ".join(self._args)
        return super().save(force_insert, force_update, using, update_fields)

    @cached_property
    def _args(self) -> tuple[str, ...]:
        """

        :return:
        :rtype: tuple[str, ...]
        """
        argument: ArgumentPair
        return tuple(argument.arg for argument in self.arguments.through.objects.all())

    @cached_property
    def command(self) -> tuple[str, ...]:
        """

        :return:
        :rtype: tuple[str, ...]
        """
        return str(self.aria2c.path), *self._args


class ArgumentPair(models.Model):
    """
    The model of Aria2 Profile Argument Pair
    """

    profile = models.ForeignKey("Aria2cProfile", on_delete=models.CASCADE)
    argument = models.ForeignKey("Argument", on_delete=models.CASCADE)
    value = models.CharField(max_length=256)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("profile", "argument"), name="unique_argument_pair"
            ),
        )
        verbose_name = "Aria2c - Argument Pair"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return f"{self.arg} ({self.profile})"

    @cached_property
    def arg(self) -> str:
        """

        :return:
        :rtype: str
        """
        return f"{self.argument}={self.value}"
