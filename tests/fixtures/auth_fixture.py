from pytest import fixture
import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fam.database.models import UserTable
from fam.utils import hash_password


@fixture
def user_login():
    email: str = "Walker"
    password: str = "123456789"

    return email, password


@fixture
def user_signup(user_login) -> None:
    return user_login


@pytest.fixture(scope="function")
def prepare_database(prepare_app, user_signup):
    # Crée un répertoire temporaire pour la base de données
    temp_dir, app_dir = prepare_app
    db_path = (app_dir / "auth.db").as_posix()

    # Configure le moteur de base de données SQLite en mémoire
    engine = create_engine(f"sqlite:///{db_path}")

    # Crée les tables en utilisant Alembic
    config = Config(
        "alembic_app.ini"
    )  # Assurez-vous que le chemin du fichier de configuration Alembic est correct
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")

    # Applique les migrations
    command.upgrade(config, "head")

    # Crée une session pour interagir avec la base de données
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Insère un utilisateur de test
    test_email, test_password = user_signup
    user = UserTable(
        email=test_email, password=hash_password(test_password), database_url=""
    )
    session.add(user)
    session.commit()

    # Assurez-vous de retourner la configuration nécessaire pour le test
    yield {
        "db_path": f"sqlite:///{db_path}",
        "session": session,
        "engine": engine,
        "temp_dir": temp_dir,
        "app_dir": app_dir,
    }

    # Nettoyage après les tests
    session.close()
    engine.dispose()
