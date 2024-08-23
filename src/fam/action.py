from pathlib import Path
import shutil
from typing import Any
from rich import print
from sqlalchemy import  create_engine, Engine
from alembic.config import Config
from alembic import command
from uuid import UUID, uuid4

from fam.database.db import DatabaseType, get_db
from fam.database.models import UserTable
from fam.database.users.models import  UserBase
from fam.database.users.schemas import AccountBM, CreateClassify
from fam.database.users import services as user_services
from fam.system.file import File
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
    
    database_url:str =  _generate_database_url(database_path)
    engine = create_engine(database_url)
    
    try:
        _create_table(engine)
        _apply_migrations(database_url)
        _initialize_default_data(database_url)
        fprint("The new database was successfully created.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la création de la base de données : {e}")
        raise
    finally:
        engine.dispose()

    return database_url

def create_session(user: UserTable) -> None:
    session: dict[str, Any] = {"session": {"user_id": user.id, "database_url": user.database_url}}

    app_dir: Path = Path(app_cli.directory.app_dir)

    sess_filename: Path = app_dir / "users" / "session.yaml"

    File.save_file(sess_filename.as_posix(), session, "yaml")
    
    
def _generate_database_url(database_path: Path) -> str:
        db_id: UUID = uuid4()

        database_url: str = f"sqlite:///{(database_path / db_id.hex).with_suffix(".db").as_posix() }"
        
        return database_url
    
def _create_table(eng: Engine) -> None:
    UserBase.metadata.create_all(bind=eng)
    
def _apply_migrations(database_url: str) -> None:
        # Configure Alembic with the new DATABASE_URL
        alembic_cfg = Config("alembic_users.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        

        # Apply Alembic migrations
        command.upgrade(alembic_cfg, "head")

def _initialize_default_data(database_url: str):
    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:
        accounts: list[AccountBM] = [
            AccountBM( name="income", description="Income account."),
            AccountBM( name="expense", description="Expense account."),
            AccountBM( name="asset", description="Asset account."),
            AccountBM( name="passive", description="Passive account."),
        ]
        classifications = [
                    CreateClassify(name="personel"),
                    CreateClassify(name="family")
                ]
        
        user_services.create_account(db, accounts)
        user_services.create_new_classification(db, classifications)
