import typer
from system import file, directory


class AppCli:
    __app__ = "Fam"
    __version__ = "1.0.0"
    __desc__ = ""

    def __init__(self) -> None:
        self._app_name: str = "Financial Advisor for Me (Fam)"
        self._version: str = "1.0.0"
        self._desc: str = "Application for financial."
        self._directory: directory.Dir = directory.Dir()
        self._file: file.File = file.File(self._directory)

    def startup(self):
        self._directory.app_dir = typer.get_app_dir(
            app_name=self._app_name, roaming=False
        )
