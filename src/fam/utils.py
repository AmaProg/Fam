from pathlib import Path
import re
from time import sleep
import time
from typing import Any
import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

console: Console = Console()


def add_command(app: typer.Typer, commands: list[dict[str, Any]]):

    for command in commands:
        app.add_typer(
            typer_instance=command.get("app", None),
            name=command.get("name", ""),
        )

    return app


def fprint(message, color: str = "cyan"):
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


def print_dev_mode() -> None:
    msg: str = "You are in development mode."

    panel: Panel = Panel(
        msg,
        title="Dev Mode",
        border_style="yellow",
        padding=(0, 1),
    )

    console.print(panel, justify="left")


def fprint_panel(msg: str, title: str, color: str = "yellow") -> None:

    panel: Panel = Panel(
        msg,
        title=title,
        border_style=color,
        padding=(0, 1),
    )

    console.print(panel, justify="left")

    time.sleep(2)


def normalize_string(s: str):
    s = s.strip().lower()
    s = re.sub(r"\W+", "", s)
    return s


def normalize_list(s: str) -> list[str]:
    return s.strip().split(",")


def message_coming_soon() -> None:
    fprint("This command is coming soon")


def is_empty_list(l: Any) -> bool:

    return True if len(l) != 0 else False
