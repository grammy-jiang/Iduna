"""
This command is going to initialize the development environment
"""
from __future__ import annotations

import pprint
from functools import cache
from pathlib import Path
from typing import Any, Optional, TypeVar

from django.apps import AppConfig as _AppConfig
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from aria2.models import Aria2c, Aria2cArgument, Aria2cInstance

AppConfig = TypeVar("AppConfig", bound=_AppConfig)

User = get_user_model()


@cache
def get_local_apps() -> tuple[AppConfig, ...]:
    """

    :return:
    :rtype: tuple[AppConfig, ...]
    """
    return tuple(
        app_config
        for app_config in apps.app_configs.values()
        if Path(app_config.path).is_relative_to(settings.BASE_DIR)
    )


ARIA2_MIGRATIONS = Path(apps.get_app_config("aria2").path) / "migrations"

SCRIPTS_KEEP: set[Path] = {
    ARIA2_MIGRATIONS / "0010_initial_aria2c.py",
    ARIA2_MIGRATIONS / "0020_initial_profile.py",
    ARIA2_MIGRATIONS / "0030_initial_instance.py",
}


class Command(BaseCommand):
    """
    initialize the development environment
    """

    help = "Initialize the development environment"

    def _remove_database(self) -> None:
        """
        remove existed databases
        :return:
        :rtype: None
        """
        self.stdout.write(
            self.style.NOTICE(
                f"The database found in settings:\n"
                f"{pprint.pformat(settings.DATABASES)}"
            )
        )
        database: dict[str, Any]
        for database in settings.DATABASES.values():
            if (
                database["ENGINE"] == "django.db.backends.sqlite3"
                and database["NAME"].is_file()  # type: ignore
            ):
                database["NAME"].unlink()  # type: ignore
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Remove existed sqlite3 database: {database['NAME']}"
                    )
                )

    def _remove_migration_scripts(self) -> None:
        """
        remove existed migration scripts
        :return:
        :rtype: None
        """
        for app in get_local_apps():
            removed_scripts: list[str] = []
            for script in app.migration_scripts:
                if script in SCRIPTS_KEEP:
                    continue
                removed_scripts.append(str(script))
                script.unlink()

            self.stdout.write(
                self.style.SUCCESS(
                    f"The migration scripts of the local app [{app.name}] are "
                    f"removed:\n"
                    f"{pprint.pformat(removed_scripts)}"
                )
            )

    def _create_migration_scripts(self) -> None:
        """
        run command makemigrations
        :return:
        :rtype: None
        """
        self.stdout.write(self.style.NOTICE("Run command makemigrations"))
        call_command("makemigrations")
        for app in get_local_apps():
            scripts = tuple(
                str(x) for x in set(app.migration_scripts).difference(SCRIPTS_KEEP)
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"The migration scripts of the local app [{app.name}] are "
                    f"created:\n"
                    f"{pprint.pformat(scripts)}"
                )
            )

    def _migrate(self) -> None:
        """
        run command migrate against each database
        :return:
        :rtype: None
        """
        for database in settings.DATABASES:
            self.stdout.write(
                self.style.NOTICE(f"Run command migrate against database [{database}]")
            )
            call_command("migrate", f"--database={database}")

    def _load_fixtures(self) -> None:
        """
        load fixtures
        :return:
        :rtype: None
        """
        for app in get_local_apps():
            self.stdout.write(
                self.style.NOTICE(
                    f"The fixtures of the local app [{app.name}] are found:\n"
                    f"{pprint.pformat(tuple(str(x) for x in app.fixtures))}"
                )
            )

            self.stdout.write(self.style.NOTICE("Start to load fixtures."))

            for i, fixture in enumerate(app.fixtures, start=1):
                call_command("loaddata", fixture)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{i}/{len(app.fixtures)}] "
                        f"Fixture is successfully loaded: {fixture}"
                    )
                )

    def _load_aria2c(self) -> None:
        """
        load aria2c from the local file system
        :return:
        :rtype: None
        """
        aria2cs = Aria2c.objects.create_from_file_system()
        paths = list(str(path) for path in aria2cs.values_list("path", flat=True))
        self.stdout.write(
            self.style.SUCCESS(
                f"Load [{aria2cs.count()}] binaries from the local file system:\n"
                f"{pprint.pformat(paths)}"
            )
        )

    def _load_arguments(self) -> None:
        """
        load arguments
        :return:
        :rtype: None
        """
        for aria2c in Aria2c.objects.all():
            arguments = Aria2cArgument.objects.create_from_aria2c(aria2c)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Load [{len(arguments)}] arguments from [{aria2c}]."
                )
            )

    def _load_instances(self) -> None:
        """
        load instances
        :return:
        :rtype: None
        """
        for aria2c in Aria2c.objects.all():
            instances = Aria2cInstance.objects.create_all_from_aria2c(aria2c)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Load [{len(instances)}] instances from [{aria2c}]:\n"
                    f"{pprint.pformat(instances)}"
                )
            )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """

        :param args:
        :type args: Any
        :param options:
        :type options: Any
        :return:
        :rtype: Optional[str]
        """
        self.stdout.write(
            self.style.NOTICE(
                "This init command is to initialize the development environment."
            )
        )

        if not settings.DEBUG:
            self.stderr.write(
                self.style.ERROR("This command only works with DEBUG mode.")
            )

        self._remove_database()
        self._remove_migration_scripts()
        self._create_migration_scripts()
        self._migrate()
        self._load_aria2c()
        self._load_arguments()
        self._load_fixtures()
        self._load_instances()
