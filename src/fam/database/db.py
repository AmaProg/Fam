from enum import Enum
from pathlib import Path
from typing import Any, Generator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from contextlib import contextmanager

from fam.database.config import load_config
from fam.cli import app_cli


class DatabaseType(Enum):
    APP = "app"
    USER = "user"


class Database:
    def __init__(self, db_type: DatabaseType, user_path: str = "") -> None:
        self._config: dict[str, Any] = self._get_config_file()
        self._database_path = self._get_database_path(db_type, user_path)
        self._database_url: str = f"sqlite:///{self._database_path}"

    def create_session(self) -> sessionmaker[Session]:
        engine = create_engine(self._database_url, echo=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        return SessionLocal

    def _get_config_file(self) -> dict[str, Any]:
        app_dir: Path = Path(app_cli.directory.app_dir)
        return load_config((app_dir / "config.yaml").as_posix())

    def _get_database_path(self, db_type: DatabaseType, user: str = "") -> str:

        if db_type == DatabaseType.APP:

            database_name: str = self._config["database"]["name"]
            app_dir: Path = Path(app_cli.directory.app_dir)

            return (app_dir / database_name).as_posix()

        else:
            return user


@contextmanager
def get_db(db_type: DatabaseType, user: str = "") -> Generator[Session, Any, Any]:
    db: Database = Database(db_type, user)
    local: sessionmaker[Session] = db.create_session()
    session = local()

    try:
        yield session
    finally:
        session.close()
