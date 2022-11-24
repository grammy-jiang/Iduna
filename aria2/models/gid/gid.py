"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
from __future__ import annotations

import logging
import pprint
from typing import Any

from django.db import models

from ..utils import TimeStampMixin

logger = logging.getLogger(__name__)


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
