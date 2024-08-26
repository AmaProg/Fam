from pathlib import Path
from time import sleep
from typing import Any

from sqlalchemy import ScalarResult
import typer
import string
import secrets
from rich import print
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def add_command(app: typer.Typer, commands: list[dict[str, Any]]):

    for command in commands:
        app.add_typer(
            typer_instance=command.get("app", None),
            name=command.get("name", ""),
        )

    return app


def fprint(message):
    color: str = "cyan"
    print(f"[{color}]Fam[/{color}]: {message}")
    sleep(0.2)


def fAborted() -> None:
    color: str = "red"
    print(f"[{color}]Aborted[/{color}]")


def verify_password(plain_password: str, hasded_password: str):
    return pwd_context.verify(plain_password, hasded_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user_dir_from_database_url(database_url: str) -> Path:
    new_database_path = database_url.replace("sqlite:///", "")

    return Path(new_database_path).parent.parent
