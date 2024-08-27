import random
from io import StringIO
from typing import Sequence

import pandas as pd
from pytest import fixture
from sqlalchemy import desc

from fam.command.creating.create import subcategory
from fam.database.users.models import (
    AccountTable,
    CategoryTable,
    ClassificationTable,
    SubCategoryTable,
    TransactionTable,
)
from fam.database.users.schemas import CreateTransactionBM
from fam.enums import BankEnum, FinancialProductEnum


@fixture
def sample_dataframe() -> pd.DataFrame:
    # Données CSV en tant que chaîne de caractères
    csv_data = """Article no,Carte no,Date de la transaction,Date de l'inscription au relevé,Montant de la transaction,Description
1,12345,20240801,20240801,100.00,Description 1
2,67890,20240802,20240802,200.00,IGA Epicerie
3,54321,20240803,20240803,300.00,Description 3
"""

    # Utiliser StringIO pour simuler un fichier CSV
    csv_file = StringIO(csv_data)

    # Lire les données CSV dans un DataFrame
    df = pd.read_csv(csv_file)

    return df


@fixture
def transaction_list_form_database():

    desc: list[str] = ["Achat café Starbucks", "Paiement facture électricité", "Loyer"]
    amount_list: list[float] = [6.50, 100.50, 700.00]
    category_list: list[str] = ["Restaurant", "Habitation", "Habitation"]
    new_transaction: CreateTransactionBM
    expense_account = 2
    personel_class = 1

    rent_id = 1
    Elect_id = 1
    Gas_id = 2

    subcategory_list: list[int] = [rent_id, Elect_id, Gas_id]
    trans_table_list: list[TransactionTable] = []

    for idx, trans_desc in enumerate(desc):
        new_transaction = CreateTransactionBM(
            description=trans_desc,
            amount=amount_list[idx],
            bank_name=BankEnum.BMO.value,
            date=20240525,
            product=FinancialProductEnum.CREDIT_CARD.value,
            account_id=expense_account,
            classification_id=personel_class,
            subcategory_id=subcategory_list[idx],
        )

        trans_table: TransactionTable = TransactionTable(**new_transaction.model_dump())

        trans_table.id = idx
        trans_table.subcategory = SubCategoryTable()
        trans_table.subcategory.category = CategoryTable()
        trans_table.subcategory.category.name = category_list[idx]

        trans_table_list.append(trans_table)

    trans_table_sequence: Sequence[TransactionTable] = trans_table_list

    return trans_table_sequence
