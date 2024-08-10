from rich import print

from fam.cli import app_cli


def display_version() -> None:
    print(f"{app_cli.app_name} version {app_cli.version}")
