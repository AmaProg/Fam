from pathlib import Path
import shutil
import sys
import typer


class Dir:
    @property
    def app_dir(self) -> str:
        return self._app

    @app_dir.setter
    def app_dir(self, value: str):
        self._app = value

    @property
    def exe(self) -> str | None:
        return self._exe

    def __init__(self) -> None:
        self._app: str = ""
        self._exe: str | None = self._get_base_dir()

    def copy_folder(self, src: Path, dest: Path):

        if not dest.exists():
            dest.mkdir(parents=True, exist_ok=True)

        for ele in src.iterdir():
            dest_path = dest / ele.name

            if ele.is_dir():
                self.copy_folder(ele, dest_path)
            else:
                if not dest_path.exists():
                    shutil.copy2(ele, dest_path)

    def _get_base_dir(self) -> str | None:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent.as_posix()
        else:
            return self._find_project_root("fam")

    def _find_project_root(self, marker_name: str) -> str | None:
        cp: Path = Path(__file__).resolve()

        while cp != cp.parent:
            if (cp / marker_name).exists():
                return (cp / marker_name).as_posix()

            cp = cp.parent
