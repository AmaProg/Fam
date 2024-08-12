from pathlib import Path
from typing import Literal

import yaml
from fam.system import directory


class File:
    def __init__(self, dir: directory.Dir) -> None:
        self._directory: directory.Dir = dir

    def create_file(self, dir_path: str, filename: str) -> None:

        file: Path = Path(dir_path) / filename

        file.touch()

    @classmethod
    def read_file(cls, path: str, type_file: Literal["yaml"]):
        with open(path, "r") as f:

            if type_file == "yaml":
                return yaml.safe_load(f)
            else:
                return f

    @classmethod
    def save_file(cls, path: str, data, type_file: Literal["yaml"]):
        with open(path, "w") as f:

            if type_file == "yaml":
                yaml.safe_dump(data, f)
