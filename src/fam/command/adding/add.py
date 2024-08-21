from pathlib import Path
from typing import Any
from typing_extensions import Annotated
from pandas import DataFrame
from sqlalchemy import ScalarResult
from typer import Typer
from tkinter import filedialog
import typer
import pandas as pd

from fam import auth
from fam.command.adding import action
from fam.database.db import DatabaseType, get_db
from fam.database.users.models import (
    CategoryTable,
    ClassificationTable,
    TransactionTable,
)
from fam.enums import BankEnum, FinancialProductEnum
from fam.utils import fprint
from fam.database.users import services as user_services

app = Typer(help="Allows you to add items to the folder.")

add_command: dict[str, Any] = {"app": app, "name": "add"}


@app.command()
def statement(
    filename: Annotated[str, typer.Option("--filename", "-f", help="")] = None,
    product: Annotated[
        FinancialProductEnum, typer.Option("--product", "-p", help="")
    ] = None,
):

    # Get user session.
    session = auth.get_user_session()

    database_url: str = session["database_url"]

    # Ask the user for which financial product the statement is
    if product is None:
        product_name: FinancialProductEnum = typer.prompt(
            type=FinancialProductEnum,
            text=f"What is the financial product {[choice.name.lower() for choice in FinancialProductEnum]}? ",
            show_choices=True,
        )

    # Ask the user which bank the statement comes from.
    bank_name: BankEnum = typer.prompt(
        type=BankEnum,
        text=f"which bank does the bank statement come from {[choice.name.lower() for choice in BankEnum]}? ",
        show_choices=False,
    )

    # Get csv file and convert to dataframe
    if filename is None:
        # open dialogFile
        csv_filename: str = filedialog.askopenfilename(
            title=f"select the statement for the {bank_name.name} bank",
            filetypes=(("CSV files", "*.csv"),),
        )
        if csv_filename == "":
            raise typer.Abort()
    else:
        csv_filename = filename

    if Path(csv_filename).suffix.lower() != ".csv":
        fprint("Invalid file format: not a CSV.")
        raise typer.Abort()

    df_csv: DataFrame = pd.read_csv(csv_filename, skiprows=1)

    with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

        # Get all category
        categories: ScalarResult[CategoryTable] = user_services.get_all_category(db)
        classifies: ScalarResult[ClassificationTable] = (
            user_services.get_all_classification(db)
        )

        # By category build category and classification choice
        cat_dict: dict[int, CategoryTable] = {}
        cat_dict.update({category.id: category for category in categories})
        cat_choice: list[str] = [
            f"{category.id}: {category.name} ({category.account.name})"
            for category in categories
        ]

        class_dict: dict[int, ClassificationTable] = {}
        class_dict.update({classify.id: classify for classify in classifies})
        class_choice: list[str] = [str(f"{classify.id} : {classify}") for classify in classifies]

        # Classify all transaction
        transactions: list[TransactionTable] = []

        for idx, transaction in df_csv.iterrows():
            # promp question for each transaction
            cat_id: int = typer.prompt(type=int, text=f"{cat_choice}\n\nSelect a category for {transaction["Description"]}",)
            cls_id: int = typer.prompt(type=int, text=f"{class_choice}\n\nSelect a class for {transaction["Description"]}",)

        # Save all transactions that have been categorized in the database

    # print success transaction
    fprint("Assignment of categories to the transaction was successfully completed.")

    # # Get de user session
    # session = auth.get_user_session()

    # database_url: str = session["database_url"]

    # # Ask the user which bank the statement comes from.
    # bank_name: BankEnum = typer.prompt(
    #     type=BankEnum,
    #     text=f"which bank does the bank statement come from {[choice.name.lower() for choice in BankEnum]}? ",
    #     show_choices=False,
    # )

    # if filename == None:

    #     # open dialogFile
    #     csv_filename: str = filedialog.askopenfilename(
    #         title=f"select the statement for the {bank_name.name} bank",
    #         filetypes=(("CSV files", "*.csv"),),
    #     )

    #     if csv_filename == "":
    #         raise typer.Abort()
    # else:
    #     csv_filename = filename

    # # check if it is cs file.
    # if Path(csv_filename).suffix.lower() != ".csv":
    #     fprint("Invalid file format: not a CSV.")
    #     raise typer.Abort()

    # df_csv: DataFrame = pd.read_csv(csv_filename, skiprows=1)

    # # assingn category for all transaction
    # with get_db(db_path=database_url, db_type=DatabaseType.USER) as db:

    #     # Get categories list
    #     cat_list: ScalarResult[CategoryTable] = user_services.get_all_category(db)
    #     classify: ScalarResult[ClassificationTable] = (
    #         user_services.get_all_classification(db)
    #     )

    #     transactions: list[TransactionTable] = action.classify_transaction(
    #         df=df_csv,
    #         bank_name=bank_name,
    #         categories=cat_list,
    #         class_transaction=classify,
    #     )

    #     # save de assignation on the database
    #     user_services.create_transaction(db, transactions)

    pass
