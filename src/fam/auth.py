from pathlib import Path
from typing import Any

from fam.system.file import File
from fam.cli import app_cli


def get_user_session() -> dict[str, Any]:
    app_dir: Path = Path(app_cli.directory.app_dir)

    sess_path: Path = app_dir / "users" / "session.yaml"

    session_data: dict[str, Any] = File.read_file(sess_path.as_posix(), "yaml")

    return session_data["session"]
