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


def build_choice(data_result: ScalarResult[Any], type: type):

    choice: list = []
    choice_dict = {}

    for data in data_result:
        choice.append(f"{data.id}: {data.name}")
        choice_dict.update({data.id: data})

    return choice, choice_dict
