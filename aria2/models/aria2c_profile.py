"""
The model of Aria2 Profile
"""
from __future__ import annotations

from django.db import models


class Aria2cProfile(models.Model):
    """
    The model of Aria2 Profile
    """

    name = models.CharField(max_length=256, primary_key=True)
    aria2c = models.ForeignKey("Aria2c", on_delete=models.CASCADE)

    arguments = models.ManyToManyField("Aria2cArgument", through="ArgumentPair")

    class Meta:
        verbose_name = "Aria2c - Profile"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self.name


class ArgumentPair(models.Model):
    """
    The model of Aria2 Profile Argument Pair
    """

    profile = models.ForeignKey("Aria2cProfile", on_delete=models.CASCADE)
    argument = models.ForeignKey("Aria2cArgument", on_delete=models.CASCADE)
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
        return f"{self.argument}={self.value} ({self.profile})"
