"""
The model of Aria2 GID Torrent
* https://aria2.github.io/manual/en/html/aria2c.html#aria2.addTorrent
"""
from __future__ import annotations

import logging

from django.db import models

from .utils import AbstractAria2cGIDTask

logger = logging.getLogger(__name__)


class Aria2cGIDTorrent(AbstractAria2cGIDTask):
    """
    This method adds a BitTorrent download by uploading a ".torrent" file. If you want
    to add a BitTorrent Magnet URI, use the aria2.addUri() method instead. torrent must
    be a base64-encoded string containing the contents of the ".torrent" file. uris is
    an array of URIs (string). uris is used for Web-seeding. For single file torrents,
    the URI can be a complete URI pointing to the resource; if URI ends with /, name in
    torrent file is added. For multi-file torrents, name and path in torrent are added
    to form a URI for each file.
    """

    torrent = models.TextField()
    uris = models.JSONField()

    class Meta:
        verbose_name = "GID - Torrent"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.torrent, self.uris if self.uris else {}, *super()._get_args()]
