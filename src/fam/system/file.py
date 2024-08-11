from pathlib import Path
from fam.system import directory


class File:
    def __init__(self, dir: directory.Dir) -> None:
        self._directory: directory.Dir = dir

    def create_file(self, dir_path: str, filename: str) -> None:

        file: Path = Path(dir_path) / filename

        file.touch()
