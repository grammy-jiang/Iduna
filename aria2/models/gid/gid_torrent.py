"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
from __future__ import annotations

import logging

from django.db import models

from .utils import AbstractAria2cGIDTask

logger = logging.getLogger(__name__)


class Aria2cGIDTorrent(AbstractAria2cGIDTask):
    """
    The model of Aria2 GID Torrent
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addTorrent
    """

    torrent = models.TextField()
    uris = models.JSONField()

    class Meta:
        verbose_name = "Aria2c - GID - Torrent"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.torrent, self.uris if self.uris else {}, *super()._get_args()]
