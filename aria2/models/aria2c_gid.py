"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
from __future__ import annotations

import pprint
from typing import TYPE_CHECKING, Any

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

    gid = models.CharField(max_length=16, primary_key=True)
    instance = models.ForeignKey("Aria2cInstance", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Aria2c - GID"

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


class AbstractAria2cGIDTask(TimeStampMixin):
    """
    The abstract model of Aria2 GID task
    """

    gid = models.OneToOneField(
        "Aria2cGID", blank=True, null=True, on_delete=models.CASCADE
    )
    instance = models.ForeignKey(
        "Aria2cInstance",
        blank=True,
        default=get_default_instance,
        null=True,
        on_delete=models.CASCADE,
    )

    secret = models.CharField(blank=True, max_length=256, null=True)
    options = models.JSONField(blank=True, null=True)
    position = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        args = [self.options if self.options else {}]
        if self.position:
            args.append(self.position)
        return args

    def create_gid(self) -> None:
        """

        :return:
        :rtype: None
        """
        args = self._get_args()
        if self.secret:
            args = [self.secret, *args]
        self.gid = Aria2cGID.objects.create(
            gid=self.instance.rpc_server_proxy.aria2.addUri(*args),
            instance=self.instance,
        )
        return self.save()


class Aria2cGIDUri(AbstractAria2cGIDTask):
    """
    The model of Aria2 GID URI
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addUri
    """

    uris = models.JSONField()

    class Meta:
        verbose_name = "Aria2c - GID - Uri"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.uris, *super()._get_args()]


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


class Aria2cGIDMetaLink(AbstractAria2cGIDTask):
    """
    The model of Aria2 GID MetaLink
    * https://aria2.github.io/manual/en/html/aria2c.html#aria2.addMetalink
    """

    metalink = models.TextField()

    class Meta:
        verbose_name = "Aria2c - GID - MetaLink"

    def _get_args(self) -> list:
        """

        :return:
        :rtype: list
        """
        return [self.metalink, *super()._get_args()]
