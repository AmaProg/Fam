from pathlib import Path
from typing import Any
from typing_extensions import Annotated
from typer import Typer

from rich import print
import typer

from fam.cli import app_cli
from fam.enums import CategorySection
from fam.utils import fAborted, fprint
from fam.database.table.category import Category

app = Typer(
    help="Creates bank accounts and expense or income categories.",
    no_args_is_help=True,
)

create_command: dict[str, Any] = {"app": app, "name": "create"}


@app.command(help="Allows you to create bank accounts.")
def account(bank, name, description):
    pass


@app.command(
    help="Allows you to create expense or income categories.",
    no_args_is_help=True,
)
def category(
    name: Annotated[str, typer.Option(..., "--name", "-n", help="Category name.")],
    category: Annotated[
        CategorySection,
        typer.Option(
            ...,
            "--category",
            "-c",
            help="Name of the category which groups the categories.",
            case_sensitive=False,
        ),
    ],
    desc: Annotated[
        str, typer.Option("--desc", "-d", help="Description of the category.")
    ] = None,
):

    try:

        # Recuperer le chemin du fichier categories et ouvrir le fichier et
        # recupere le contenue.

        app_dir: Path = Path(app_cli.directory.app_dir)
        categories_file: Path = app_dir / "database" / "table" / "category.yaml"
        # data: dict[str, Any] = {}

        # yaml_data: dict = app_cli.file.read_file(categories_file.as_posix(), "yaml")
        # category_data: dict[str, Any] = {"name": name, "description": desc}

        cat: Category = Category(categories_file.as_posix())

        cat.insert_data(name, desc, category.value)

        cat.submit()

        print("")

        # cat.add_data(name, desc, category)

        # cat.submit()

        # Verifier si la categorie existe deja
        # if yaml_data["categories"] is None:

        #     # Ajouter la categorie dans le fichier et le sauvegarder.

        #     category_header: str = category

        #     data[category_header] = [category_data]

        #     yaml_data["categories"] = [data]

        # else:

        #     cat_table: list = yaml_data["categories"]

        #     for idx, row in enumerate(cat_table):

        #         if category in row:

        #             cat_list: list = row[category]

        #             for idx, cat in enumerate(cat_list):

        #                 if cat["name"] == name:
        #                     fprint(
        #                         f"The category '[yellow]{name}[/yellow]' already exists for the '[yellow]{category}[/yellow]' section"
        #                     )
        #                     raise typer.Abort()

        #             cat_list.append(category_data)
        #             break

        #     category_header: str = category

        #     data[category_header] = [category_data]

        #     yaml_data["categories"].append(data)

        # app_cli.file.save_file(categories_file.as_posix(), yaml_data, "yaml")

        # print un message qui indique a l utilisateur que le l'ajoute a ete
        # reussi avec success
        color: str = "green"
        fprint(f"The category '[{color}]{name}[/{color}]' was added successfully.")

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        print(e)

    pass
