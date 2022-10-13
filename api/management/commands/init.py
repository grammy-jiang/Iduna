"""
This command is going to initialize the development environment
"""
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


SCRIPTS_KEEP: tuple[Path, ...] = tuple()


def get_migration_scripts(app: AppConfig) -> tuple[Path, ...]:
    """

    :param app:
    :type app: AppConfig
    :return:
    :rtype: tuple[Path, ...]
    """
    migrations = Path(app.path) / "migrations"
    if not migrations.is_dir():
        raise NotADirectoryError
    return tuple(
        script
        for script in migrations.iterdir()
        if script.is_file() and script.stem != "__init__" and script.suffix == ".py"
    )


def get_fixtures(app: AppConfig) -> list[Path]:
    """

    :param app:
    :type app: AppConfig
    :return:
    :rtype: list[Path]
    """
    fixtures = Path(app.path) / "fixtures"
    if not fixtures.is_dir():
        raise NotADirectoryError
    return sorted(
        fixture for fixture in fixtures.iterdir() if fixture.suffix in {".yaml", ".yml"}
    )


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
            scripts = get_migration_scripts(app)
            if not scripts:
                continue
            for script in scripts:
                if script in SCRIPTS_KEEP:
                    continue
                script.unlink()
            self.stdout.write(
                self.style.SUCCESS(
                    f"The migration scripts of the local app [{app.name}] are "
                    f"removed:\n"
                    f"{pprint.pformat(tuple(str(i) for i in scripts))}"
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
            scripts = get_migration_scripts(app)
            if not scripts:
                continue
            self.stdout.write(
                self.style.SUCCESS(
                    f"The migration scripts of the local app [{app.name}] are "
                    f"created:\n"
                    f"{pprint.pformat(tuple(str(x) for x in scripts))}"
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
            try:
                fixtures = get_fixtures(app)
            except NotADirectoryError:
                continue

            if not fixtures:
                continue

            self.stdout.write(
                self.style.NOTICE(
                    f"The fixtures of the local app [{app.name}] are found:\n"
                    f"{pprint.pformat(tuple(str(x) for x in fixtures))}"
                )
            )

            self.stdout.write(self.style.NOTICE("Start to load fixtures."))

            for i, fixture in enumerate(fixtures, start=1):
                call_command("loaddata", fixture)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"[{i}/{len(fixtures)}] "
                        f"Fixture is successfully loaded: {fixture}"
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
        self._load_fixtures()
