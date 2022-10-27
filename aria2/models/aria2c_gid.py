"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
import pprint
from typing import Any, Iterable, Optional

from django.db import models


class Aria2cGID(models.Model):
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
