from pathlib import Path
from rich import print

from fam.system.file import File
from fam.utils import fprint
from fam.cli import app_cli


def init_app_dir() -> None:
    try:
        app_cli.startup()

        init_file: Path = Path(app_cli.directory.app_dir) / "init"

        if init_file.exists():
            msg = (
                "The workspace has already been initialized. "
                "if you want to reset the workspace to zero please use the [green]reset[/green] command"
            )

            fprint(msg)
        else:
            fprint("Prepare the workspace ...")

            if app_cli.directory.exe is None:
                raise ValueError("The file is not existe")

            app: Path = Path(app_cli.directory.exe) / "static" / "template" / "app"

            app_cli.directory.copy_folder(app, Path(app_cli.directory.app_dir))

            init_file.touch()

            fprint("The workspace was successfully created")

    except Exception as e:
        print(e)
