import typer


class Dir:
    @property
    def app_dir(self) -> str:
        return self._app

    @app_dir.setter
    def app_dir(self, value: str):
        self._app = value

    def __init__(self) -> None:
        self._app: str = ""
