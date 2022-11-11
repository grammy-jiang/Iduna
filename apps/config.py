"""Custom AppConfig for Iduna"""
from pathlib import Path

from django.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
    """Custom AppConfig for Iduna"""

    @property
    def migration_scripts(self) -> tuple[Path, ...]:
        """get the migration scripts of the current application

        :return:
        :rtype: tuple[Path, ...]
        """
        try:
            return tuple(
                script
                for script in (Path(self.path) / "migrations").iterdir()
                if script.is_file()
                and script.stem != "__init__"
                and script.suffix == ".py"
            )
        except FileNotFoundError:
            return ()

    @property
    def fixtures(self) -> list[Path]:
        """get the fixtures of the current application

        :return:
        :rtype: list[Path]
        """
        try:
            return sorted(
                fixture
                for fixture in (Path(self.path) / "fixtures").iterdir()
                if fixture.is_file() and fixture.suffix in {".yaml", ".yml"}
            )
        except FileNotFoundError:
            return []
