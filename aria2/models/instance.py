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
    from .argument import Argument as TArgument
    from .binary import Binary as TBinary
    from .profile import ArgumentPair as TArgumentPair
    from .profile import Profile as TProfile


logger = logging.getLogger(__name__)


class QuerySet(models.QuerySet):
    """
    custom QuerySet to fit aria2c
    """

    def create_from_pid(self, pid: int | str) -> Instance:
        """

        :param pid:
        :type pid: int | str
        :return:
        :rtype: Instance
        """
        Binary: TBinary = apps.get_model("aria2", "Binary")
        command = Binary.get_command(pid)
        binary, _ = Binary.objects.get_or_create(path=command.split(maxsplit=1)[0])
        return self.create(pid=pid, command=command, binary=binary)

    def create_all_from_aria2c(self, binary: TBinary) -> tuple[Instance, ...]:
        """

        :param binary:
        :type binary: TBinary
        :return:
        :rtype: tuple[Aria2cInstance, ...]
        """
        return tuple(
            self.create(pid=pid, command=binary.get_command(pid), binary=binary)
            for pid in binary.get_pids()
        )

    def create_from_profile(self, profile: TProfile) -> Instance:
        """

        :param profile:
        :type profile: Profile
        :return:
        :rtype: Instance
        """
        command = " ".join(profile.command)
        try:
            return self.get(command=command)
        except Instance.DoesNotExist:
            with subprocess.Popen(profile.command):
                start = datetime.now()
                while True:
                    try:
                        pid = profile.binary.get_pid(command)
                    except CommandNotFound as exc:
                        if (datetime.now() - start) > timedelta(seconds=30):
                            raise CommandExecutionFailed from exc
                        continue
                    return self.create(
                        pid=pid, command=command, binary=profile.binary, profile=profile
                    )


Manager = models.Manager.from_queryset(QuerySet)


class Instance(models.Model):
    """
    The model of Aria2 instance
    """

    pid = models.IntegerField(primary_key=True)
    command = models.CharField(max_length=256, unique=True)

    binary = models.ForeignKey("Binary", on_delete=models.CASCADE)
    profile = models.OneToOneField(
        "Profile", blank=True, null=True, on_delete=models.CASCADE
    )

    effective_user_name = models.CharField(blank=True, max_length=256, null=True)
    version = models.CharField(blank=True, max_length=256, null=True)
    session_id = models.CharField(blank=True, max_length=256, null=True)
    objects = Manager()

    class Meta:
        verbose_name = "Instance"

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
        Profile: TProfile = apps.get_model("aria2", "Profile")
        if not self.profile:
            self.profile = Profile.objects.get(args=self.command.split(maxsplit=1)[-1])
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
        Argument: TArgument = apps.get_model("aria2", "Argument")
        rpc_listen_port = Argument.objects.get(long_argument="--rpc-listen-port")
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
