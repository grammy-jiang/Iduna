"""
The model of Aria2 GID URI
* https://aria2.github.io/manual/en/html/aria2c.html#aria2.addUri
"""
from __future__ import annotations

import logging

from django.db import models

from .utils import AbstractGIDTask

logger = logging.getLogger(__name__)


class GIDUri(AbstractGIDTask):
    """
    This method adds a new download. uris is an array of HTTP/FTP/SFTP/BitTorrent URIs
    (strings) pointing to the same resource. If you mix URIs pointing to different
    resources, then the download may fail or be corrupted without aria2 complaining.
    When adding BitTorrent Magnet URIs, uris must have only one element and it should be
    BitTorrent Magnet URI.
    """

    uris = models.JSONField()

    class Meta:
        verbose_name = "GID - Uri"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.uris, *super()._get_args()]
