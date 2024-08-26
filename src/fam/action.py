from io import StringIO
from pathlib import Path
import shutil
from typing import Any
from rich import print
from sqlalchemy import  create_engine, Engine
from alembic.config import Config
from alembic import command
from uuid import UUID, uuid4
from alembic.script import ScriptDirectory

import typer

from fam import utils
from fam.database.db import DatabaseType, get_db
from fam.database.models import UserTable
from fam.database.schemas import CreateUser
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

            init_file.touch(exist_ok=False)

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
    try:
        app_dir: Path = Path(app_cli.directory.app_dir)
    
        users_folder: Path = app_dir / "users" / id
        
        users_folder.mkdir(exist_ok=False)

        return users_folder
    
    except Exception as e:
        print(f"Error creating folder {e}")
        raise typer.Abort()

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
        raise typer.Abort()
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

        database_url: str = f"sqlite:///{(database_path / "db" / db_id.hex).with_suffix(".db").as_posix() }"
        
        return database_url
    
def _create_table(eng: Engine) -> None:
    UserBase.metadata.create_all(bind=eng)
    
def _apply_migrations(database_url: str) -> None:
        # Configure Alembic with the new DATABASE_URL
        alembic_cfg = Config("alembic_users.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        alembic_cfg.set_main_option("script_location", "alembic/users")
        
        script = ScriptDirectory.from_config(alembic_cfg)
        latest_script = script.get_current_head()
        current_revision = latest_script
        
        # Apply Alembic migrations
        if current_revision is not None:
            command.upgrade(alembic_cfg, "heads")

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

def create_file(user_folder: Path) -> None:
    try:
        filename: list[str] = [
            "transaction_rule.yaml"
        ]
        
        for file in filename:
            (user_folder / file).touch(exist_ok=False)
    except Exception as e:
        print(e)
        raise typer.Abort()
        
def create_folder(user_folder: Path) -> None:
    try:
        foldername: list[str] = [
        "db"
    ]
    
        for folder in foldername:
            (user_folder / folder).mkdir(exist_ok=False)
    
    except Exception as e:
        print(e)
        raise typer.Abort()
    
def init_user_workspace(id: UUID) -> str:
    
    # Create the user folder with unique ID.
    user_dir: Path = create_new_user_folder(id.hex)
    
    create_file(user_dir)
    
    create_folder(user_dir)
    
    # Create a new sql database for the user.
    database_url = create_new_database(user_dir)
    
    return database_url

def init_user_account(user_email: str, user_pwd: str) -> CreateUser:
    # Create a unique ID.
    id: UUID = uuid4()
    
    database_url: str = init_user_workspace(id)

    # crypt the password
    hash_pwd: str = utils.hash_password(user_pwd)
    
    # create a new user in the app database
    new_user: CreateUser = CreateUser(
        email=user_email,
        password=hash_pwd,
        database_url=database_url, 
    )
    
    return new_user
