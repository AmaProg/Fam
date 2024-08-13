from pathlib import Path
import shutil
from rich import print
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from uuid import UUID, uuid4

from fam.database.users.models import UserBase
from fam.utils import fprint
from fam.cli import app_cli


def init_app_dir() -> None:
    try:
        app_cli.startup()

        init_file: Path = Path(app_cli.directory.app_dir) / "init"

        if init_file.exists():
            msg = (
                "The app has already been initialized. "
                "if you want to reset the app to zero please use the [green]fam reset[/green] command"
            )

            fprint(msg)
        else:
            fprint("Prepare the app ...")

            if app_cli.directory.exe is None:
                raise ValueError("The file is not existe")

            app: Path = Path(app_cli.directory.exe) / "static" / "template" / "app"

            app_cli.directory.copy_folder(app, Path(app_cli.directory.app_dir))

            init_file.touch()

            fprint("The app was successfully created")

    except Exception as e:
        print(e)


def reset_app(app_dir_path: Path) -> None:
    msg: str = "The app was successfully deleted"

    shutil.rmtree(app_dir_path.as_posix())
    fprint(msg)
    init_app_dir()


def delete_app(app_dir_path: Path) -> None:
    msg: str = "The app was successfully deleted"
    shutil.rmtree(app_dir_path.as_posix())
    fprint(msg)


def create_new_user_folder(id: str) -> Path:
    app_dir: Path = Path(app_cli.directory.app_dir)
    users_folder: Path = app_dir / "users" / id
    users_folder.mkdir(exist_ok=True)

    return users_folder


def create_new_database(database_path: Path) -> str:
    
    db_id: UUID = uuid4()

    database_url: str = f"sqlite:///{(database_path / db_id.hex).with_suffix(".db").as_posix() }"

    # Generate DATABASE_URL for the user
    engin = create_engine(database_url)


    # Create the tables if they don't exist
    UserBase.metadata.create_all(bind=engin)

    # Configure Alembic with the new DATABASE_URL
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)

    # Apply Alembic migrations
    command.upgrade(alembic_cfg, "head")
    
    return db_id.hex
