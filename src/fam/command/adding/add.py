from pathlib import Path
from typing import Any, Sequence
from typing_extensions import Annotated
from pandas import DataFrame
from typer import Typer
import typer

from fam import auth
from fam.command.adding import action
from fam.command.utils import build_choice, prompt_choice
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import (
    AccountNicknameTable,
)
from fam.enums import BankEnum, FinancialProductEnum
from fam.os.file import File
from fam.utils import fAborted, fprint
from fam.database.users import service, services as user_services

app = Typer(help="Allows you to add items to the folder.")

add_command: dict[str, Any] = {"app": app, "name": "add"}


@app.command()
def statement(
    bank: Annotated[
        BankEnum,
        typer.Option(
            "--bank",
            "-b",
            help="Name of the bank that generated the bank statement.",
            prompt="which bank does the bank statement come from?",
            show_choices=True,
            case_sensitive=False,
        ),
    ],
    product: Annotated[
        FinancialProductEnum,
        typer.Option(
            "--product",
            "-p",
            help="",
            prompt="What is the financial product?",
            show_choices=True,
            case_sensitive=False,
        ),
    ],
    filename: Annotated[
        str,
        typer.Option(
            "--filename", "-f", help="Path of the bank statement in csv format."
        ),
    ] = "",
):
    try:
        # Get user session.
        database_url: str = auth.get_user_database_url()

        # Get csv file and convert to dataframe
        csv_filename: str = File.open_dialog(bank) if filename == "" else filename

        if csv_filename == "":
            raise typer.Abort()

        if Path(csv_filename).suffix.lower() != ".csv":
            fprint("Invalid file format: not a CSV.")
            raise typer.Abort()

        df_csv: DataFrame | None = File.read_csv_by_bank(csv_filename, bank)

        if df_csv is None:
            fprint(f"The {bank.value} bank csv file has been corrupted.")
            raise typer.Abort()

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            db_nickname: Sequence[AccountNicknameTable] = (
                service.account_nickname.get_account_nickname(db)
            )
            nickname_dict, nickname_choice = build_choice(db_nickname, "nickname")

            while True:
                nickname_id: int = prompt_choice(
                    nickname_choice, "Select the nickname", ""
                )
                nickname: AccountNicknameTable = nickname_dict.get(nickname_id, None)

                if nickname is not None:
                    break

            action.add_new_statement(
                db=db,
                database_url=database_url,
                bank=bank,
                df=df_csv,
                product=product,
                nickname_id=nickname.id,
            )

        fprint(
            "Assignment of categories to the transaction was successfully completed."
        )

    except FileNotFoundError:
        fprint("Please log in")
        fAborted()

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        fprint(e)


@app.command(help="Allows you to add a banking institution.")
def institution(
    name: Annotated[
        str,
        typer.Option(
            "--name",
            "-n",
            help="",
            prompt="What is the name of the institution?",
        ),
    ] = None,  # type: ignore
):
    # Get user datbase url
    database_url: str = auth.get_user_database_url()

    try:

        with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

            # Add institution in the database
            service.banking_institution.create_new_bank_institution_by_name(
                db=db,
                institution_name=name,
            )

            fprint("The banking institution was successfully added")

    except Exception as e:
        fprint(e)
