"""
The model of Aria2 Instance
"""
from __future__ import annotations

import logging
import subprocess
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Iterable, Optional
from urllib.parse import ParseResult, urlunparse
from xmlrpc.client import ServerProxy

from django.apps import apps
from django.db import models
from django.utils.functional import cached_property

from ..exceptions import CommandExecutionFailed, CommandNotFound

if TYPE_CHECKING:
    from .aria2c_argument import Aria2cArgument as TAria2cArgument
    from .aria2c_profile import ArgumentPair as TArgumentPair
    from .aria2c_profile import Aria2cProfile as TAria2cProfile
    from .binary import Aria2c as TAria2c


logger = logging.getLogger(__name__)


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit aria2c
    """

    def create_from_pid(self, pid: int | str) -> Aria2cInstance:
        """

        :param pid:
        :type pid: int | str
        :return:
        :rtype: Aria2cInstance
        """
        Aria2c: TAria2c = apps.get_model("aria2", "Aria2c")
        command = Aria2c.get_command(pid)
        aria2c, _ = Aria2c.objects.get_or_create(path=command.split(maxsplit=1)[0])
        return self.create(pid=pid, command=command, aria2c=aria2c)

    def create_all_from_aria2c(self, aria2c: TAria2c) -> tuple[Aria2cInstance, ...]:
        """

        :param aria2c:
        :type aria2c: TAria2c
        :return:
        :rtype: tuple[Aria2cInstance, ...]
        """
        return tuple(
            self.create(pid=pid, command=aria2c.get_command(pid), aria2c=aria2c)
            for pid in aria2c.get_pids()
        )

    def create_from_profile(self, profile: TAria2cProfile) -> Aria2cInstance:
        """

        :param profile:
        :type profile: TAria2cProfile
        :return:
        :rtype: Aria2cInstance
        """
        command = " ".join(profile.command)
        try:
            return self.get(command=command)
        except Aria2cInstance.DoesNotExist:
            with subprocess.Popen(profile.command):
                start = datetime.now()
                while True:
                    try:
                        pid = profile.aria2c.get_pid(command)
                    except CommandNotFound as exc:
                        if (datetime.now() - start) > timedelta(seconds=30):
                            raise CommandExecutionFailed from exc
                        continue
                    return self.create(
                        pid=pid, command=command, aria2c=profile.aria2c, profile=profile
                    )


Manager = models.Manager.from_queryset(QuerySet)


class Aria2cInstance(models.Model):
    """
    The model of Aria2 instance
    """

    pid = models.IntegerField(primary_key=True)
    command = models.CharField(max_length=256, unique=True)

    aria2c = models.ForeignKey("Aria2c", on_delete=models.CASCADE)
    profile = models.OneToOneField(
        "Aria2cProfile", blank=True, null=True, on_delete=models.CASCADE
    )

    effective_user_name = models.CharField(blank=True, max_length=256, null=True)
    version = models.CharField(blank=True, max_length=256, null=True)
    session_id = models.CharField(blank=True, max_length=256, null=True)
    objects = Manager()

    class Meta:
        verbose_name = "Aria2c - Instance"

    def delete(
        self, using: Any = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        """

        :param using:
        :type using: Any
        :param keep_parents:
        :type keep_parents: bool
        :return:
        :rtype: tuple[int, dict[str, int]]
        """
        try:
            self.rpc_server_proxy.aria2.shutdown()
        except ConnectionRefusedError as exc:
            logger.exception(exc)
        return super().delete(using, keep_parents)

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
        Aria2cProfile: TAria2cProfile = apps.get_model("aria2", "Aria2cProfile")
        if not self.profile:
            self.profile = Aria2cProfile.objects.get(
                args=self.command.split(maxsplit=1)[-1]
            )
        if not self.effective_user_name:
            self.effective_user_name = (
                subprocess.check_output(
                    ["ps", "-p", str(self.pid), "-o", "euser", "--no-headers"]
                )
                .decode()
                .strip()
            )
        if not self.version:
            self.version = self.rpc_server_proxy.aria2.getVersion()["version"]
        if not self.session_id:
            self.session_id = self.rpc_server_proxy.aria2.getSessionInfo()["sessionId"]
        return super().save(force_insert, force_update, using, update_fields)

    @cached_property
    def rpc_server_address(self) -> str:
        """

        :return:
        :rtype: str
        """
        Aria2cArgument: TAria2cArgument = apps.get_model("aria2", "Aria2cArgument")
        rpc_listen_port = Aria2cArgument.objects.get(long_argument="--rpc-listen-port")
        ArgumentPair: TArgumentPair = self.profile.arguments.through
        port = ArgumentPair.objects.get(argument=rpc_listen_port).value
        url = ParseResult(
            scheme="http",
            netloc=f"localhost:{port}",
            path="rpc",
            params="",
            query="",
            fragment="",
        )
        return urlunparse(url)

    @cached_property
    def rpc_server_proxy(self) -> ServerProxy:
        """
        find all methods of aria2 rpc methods
        * https://aria2.github.io/manual/en/html/aria2c.html#methods
        :return:
        :rtype: ServerProxy
        """
        return ServerProxy(self.rpc_server_address)

    @property
    def cpu(self) -> Optional[float]:
        """

        :return:
        :rtype: Optional[float]
        """
        try:
            return float(
                subprocess.check_output(
                    ["ps", "-p", str(self.pid), "-o", "%cpu", "--no-headers"]
                )
                .decode()
                .strip()
            )
        except subprocess.CalledProcessError as exc:
            logger.exception(exc)

    @property
    def mem(self) -> Optional[str]:
        """

        :return:
        :rtype: Optional[str]
        """
        try:
            return (
                subprocess.check_output(
                    ["ps", "-p", str(self.pid), "-o", "%mem", "--no-headers"]
                )
                .decode()
                .strip()
            )
        except subprocess.CalledProcessError as exc:
            logger.exception(exc)

    @property
    def elapsed_time(self) -> Optional[timedelta]:
        """

        :return:
        :rtype: Optional[timedelta]
        """
        try:
            return timedelta(
                seconds=int(
                    subprocess.check_output(
                        ["ps", "-p", str(self.pid), "-o", "etimes", "--no-headers"]
                    )
                    .decode()
                    .strip()
                )
            )
        except subprocess.CalledProcessError as exc:
            logger.exception(exc)

    @property
    def cumulative_cpu_times(self) -> Optional[timedelta]:
        """

        :return:
        :rtype: Optional[timedelta]
        """
        try:
            return timedelta(
                seconds=int(
                    subprocess.check_output(
                        ["ps", "-p", str(self.pid), "-o", "cputimes", "--no-headers"]
                    )
                    .decode()
                    .strip()
                )
            )
        except subprocess.CalledProcessError as exc:
            logger.exception(exc)
