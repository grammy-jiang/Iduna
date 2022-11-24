"""
The model of Aria2 GID MetaLink
* https://aria2.github.io/manual/en/html/aria2c.html#aria2.addMetalink
"""
from __future__ import annotations

import logging

from django.db import models

from .utils import AbstractAria2cGIDTask

logger = logging.getLogger(__name__)


class Aria2cGIDMetaLink(AbstractAria2cGIDTask):
    """
    This method adds a Metalink download by uploading a ".metalink" file. metalink is a
    base64-encoded string which contains the contents of the ".metalink" file.
    """

    metalink = models.TextField()

    class Meta:
        verbose_name = "GID - MetaLink"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.metalink, *super()._get_args()]
