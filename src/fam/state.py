from contextlib import _GeneratorContextManager
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker, Session


@dataclass
class State:
    verbose: bool = False


@dataclass
class Context:
    db: _GeneratorContextManager[Session, None, None]
    database_url: str | None = None
