import typer
from fam.system import file, directory


class AppCli:

    @property
    def app_name(self) -> str:
        return self._app_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def desc(self) -> str:
        return self._desc

    @property
    def directory(self) -> directory.Dir:
        return self._directory

    @property
    def file(self) -> file.File:
        return self._file

    def __init__(self) -> None:
        self._app_name: str = "Financial Advisor for Me"
        self._version: str = "1.0.0"
        self._desc: str = "Application for financial."
        self._directory: directory.Dir = directory.Dir()
        self._file: file.File = file.File(self._directory)

    def startup(self):
        self._directory.app_dir = typer.get_app_dir(
            app_name=self._app_name, roaming=False
        )


app_cli: AppCli = AppCli()
