"""
The model of Aria2 GID

Aria2 identifies each download by the ID called GID. The GID must be hex string of 16
characters, thus [0-9a-fA-F] are allowed and leading zeros must not be stripped. The GID
all 0 is reserved and must not be used. The GID must be unique, otherwise error is
reported and the download is not added.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.db import models

from ..utils import TimeStampMixin
from . import GID

if TYPE_CHECKING:
    from ..instance import Instance as TInstance

logger = logging.getLogger(__name__)


def get_default_instance() -> TInstance:
    """

    :return:
    :rtype: Instance
    """
    Instance: TInstance = apps.get_model("aria2", "Instance")
    return Instance.objects.get(profile__name=settings.ARIA2_DEFAULT_INSTANCE)


class AbstractGIDTask(TimeStampMixin):
    """
    The abstract model of Aria2 GID task
    """

    gid = models.OneToOneField("GID", blank=True, null=True, on_delete=models.CASCADE)
    instance = models.ForeignKey(
        "Instance",
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
        self.gid = GID.objects.create(
            gid=self.instance.rpc_server_proxy.aria2.addUri(*args),
            instance=self.instance,
        )
        return self.save()
