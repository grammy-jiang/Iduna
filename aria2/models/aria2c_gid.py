"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
from __future__ import annotations

import pprint
from typing import TYPE_CHECKING, Any, Iterable, Optional

from django.apps import apps
from django.conf import settings
from django.db import models

from .utils import TimeStampMixin

if TYPE_CHECKING:
    from .aria2c_instance import Aria2cInstance


class Aria2cGID(TimeStampMixin):
    """
    The model of Aria2 GID
    """

    gid = models.CharField(blank=True, max_length=16, null=True)

    uris = models.JSONField()
    options = models.JSONField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)

    instance = models.ForeignKey("Aria2cInstance", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Aria2c - GID"

    def __str__(self) -> str:
        """

        :return:
        :rtype: str
        """
        return pprint.pformat(self.uris)

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
        if self.gid:
            return None
        super().save(force_insert, force_update, using, update_fields)
        self.gid = self.instance.rpc_server_proxy.aria2.addUri(self.uris)
        return super().save(force_insert, force_update, using, update_fields)

    @property
    def status(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self._verbose_status["status"]

    @property
    def _verbose_status(self) -> dict[str, Any]:
        """

        :return:
        :rtype: dict[str, Any]
        """
        return self.instance.rpc_server_proxy.aria2.tellStatus(self.gid)

    @property
    def verbose_status(self) -> str:
        """

        :return:
        :rtype: str
        """
        return pprint.pformat(self._verbose_status)

    @property
    def total_length(self) -> int:
        """

        :return:
        :rtype: int
        """
        return self._verbose_status["totalLength"]

    @property
    def completed_length(self) -> int:
        """

        :return:
        :rtype: int
        """
        return self._verbose_status["completedLength"]

    @property
    def dir(self) -> str:
        """

        :return:
        :rtype: str
        """
        return self._verbose_status["dir"]


def get_default_instance() -> Aria2cInstance:
    """

    :return:
    :rtype: Aria2cInstance
    """
    Aria2cInstance = apps.get_model("aria2", "Aria2cInstance")
    return Aria2cInstance.objects.get(profile__name=settings.ARIA2_DEFAULT_INSTANCE)


class Aria2cGIDUri(TimeStampMixin):
    """
    The model of Aria2 GID URI
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addUri
    """

    gid = models.OneToOneField(
        "Aria2cGID", blank=True, null=True, on_delete=models.CASCADE
    )
    instance = models.ForeignKey(
        "Aria2cInstance", default=get_default_instance, on_delete=models.CASCADE
    )

    uris = models.JSONField()
    options = models.JSONField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Aria2c - GID - Uri"


class Aria2cGIDTorrent(TimeStampMixin):
    """
    The model of Aria2 GID Torrent
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addTorrent
    """

    gid = models.OneToOneField(
        "Aria2cGID", blank=True, null=True, on_delete=models.CASCADE
    )
    instance = models.ForeignKey(
        "Aria2cInstance", default=get_default_instance, on_delete=models.CASCADE
    )

    torrent = models.TextField()
    uris = models.JSONField()
    options = models.JSONField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Aria2c - GID - Torrent"


class Aria2cGIDMetaLink(TimeStampMixin):
    """
    The model of Aria2 GID MetaLink
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addMetalink
    """

    gid = models.OneToOneField(
        "Aria2cGID", blank=True, null=True, on_delete=models.CASCADE
    )
    instance = models.ForeignKey(
        "Aria2cInstance", default=get_default_instance, on_delete=models.CASCADE
    )

    metalink = models.TextField()
    options = models.JSONField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Aria2c - GID - MetaLink"
