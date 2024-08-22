from enum import Enum
from pathlib import Path
from typing import Any, Generator
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from contextlib import contextmanager

from fam.database.config import load_config
from fam.cli import app_cli


class DatabaseType(Enum):
    APP = "app"
    USER = "user"


def get_db_app() -> str:
    app_dir: Path = Path(app_cli.directory.app_dir)
    config_filename: dict[str, Any] = load_config((app_dir / "config.yaml").as_posix())
    database_name: str = config_filename["database"]["name"]

    return f"sqlite:///{(app_dir / database_name).as_posix()}"


@contextmanager
def get_db(db_path: str = "", db_type: DatabaseType = DatabaseType.APP):

    if db_type == DatabaseType.APP:
        db_path = get_db_app()

    database_url: str = db_path

    engine = create_engine(database_url, echo=False)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session: Session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        engine.dispose()
