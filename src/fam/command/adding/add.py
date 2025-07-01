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
from fam.utils import fAborted, fprint, fprint_panel
from fam.database.users import service, services as user_services
from fam.log.log import logger, log_verbose, State
from fam.state import Context

app = Typer(help="Allows you to add files to the database.", no_args_is_help=True)

add_command: dict[str, Any] = {"app": app, "name": "add"}


@app.command(help="Allows to retrieve bank statement information.")
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
        # database_url: str = auth.get_user_database_url()

        # Get csv file and convert to dataframe
        csv_filename: str = File.open_dialog(bank) if filename == "" else filename

        with Context.db as db:

            db_nickname: Sequence[AccountNicknameTable] = (
                service.account_nickname.get_account_nickname(db)
            )

            if not db_nickname:
                fprint("Nickname not found. Please create one.")
                raise typer.Abort()

            nickname_dict, nickname_choice = build_choice(db_nickname, "nickname")

            while True:
                nickname_id: int = prompt_choice(
                    nickname_choice, "Select the nickname", ""
                )
                nickname: AccountNicknameTable = nickname_dict.get(nickname_id, None)

                if nickname is not None:
                    break

            if csv_filename == "":
                logger.error("The csv file is empty")
                raise typer.Abort()

            if Path(csv_filename).suffix.lower() != ".csv":
                logger.error("Invalid file format: not a CSV.")
                raise typer.Abort()
            log_verbose(f"bank statement retrieve: {Path(csv_filename).name}")

            df_csv: DataFrame | None = File.read_csv_by_bank(csv_filename, bank)
            log_verbose(df_csv)

            if df_csv is None:
                logger.error(f"The {bank.value} bank csv file has been corrupted.")
                raise typer.Abort()

            action.add_new_statement(
                db=db,
                bank=bank,
                df=df_csv,
                product=product,
                nickname_id=nickname.id,
            )

        fprint(
            "Assignment of categories to the transaction was successfully completed."
        )

    except FileNotFoundError:
        logger.error("Please log in")
        fAborted()

    except typer.Abort as e:
        fAborted()

    except Exception as e:
        logger.error(e)


# @app.command(help="Allows you to add a bank statement template")
# def institution(
#     name: Annotated[
#         str,
#         typer.Option(
#             "--name",
#             "-n",
#             help="",
#             prompt="What is the name of the institution?",
#         ),
#     ] = None,  # type: ignore
# ):
#     # Get user datbase url
#     database_url: str = auth.get_user_database_url()

#     try:

#         with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

#             # 1. Demander a l'utilisateur le nom de la banque
#             # 2. Demande a l'utilisateur les informatins suivante:
#             #    - entete de la date de transaction
#             #    - entete de la date d'enregistrement
#             #    - entete du montant de la transaction
#             #    - enten de la description de la transaction
#             # 3. tu sauvegarde les informations en format json en ayant le nom de la banque en nom de fichier.
#             # 4. afficher que les donnees ont ete sauvegarder avec success.

#             # Add institution in the database
#             service.banking_institution.create_new_bank_institution_by_name(
#                 db=db,
#                 institution_name=name,
#             )

#             fprint("The banking institution was successfully added")

#     except Exception as e:
#         fprint(e)


@app.callback()
def main(verbose: bool = False):

    if verbose:
        print("Will write verbose output")
        State.verbose = True
