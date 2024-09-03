from datetime import datetime
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
from fam.database.users.schemas import (
    CreateClassify,
    CreateSubCategory,
    CreateTransactionBM,
)
from fam.enums import BankEnum, FinancialProductEnum


@fixture
def BMO_CSV_dataframe() -> pd.DataFrame:
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
def account_from_database() -> AccountTable:
    account: AccountTable = AccountTable()

    return account


@fixture
def transaction_list_form_database():

    desc: list[str] = ["Achat café Starbucks", "Paiement facture électricité", "Loyer"]
    amount_list: list[float] = [6.50, 100.50, 700.00]
    category_list: list[str] = ["Restaurant", "Habitation", "Habitation"]
    data_list: list[str] = ["20240115", "20240120", "20240215"]
    new_transaction: CreateTransactionBM
    expense_account = 2
    personel_class = 1

    rent_id = 1
    Elect_id = 1
    Gas_id = 2

    subcategory_list: list[int] = [rent_id, Elect_id, Gas_id]
    trans_table_list: list[TransactionTable] = []

    for idx, trans_desc in enumerate(desc):

        date_format: datetime = datetime.strptime(data_list[idx], "%Y%m%d")

        new_transaction = CreateTransactionBM(
            description=trans_desc,
            amount=amount_list[idx],
            bank_name=BankEnum.BMO.value,
            date=int(date_format.timestamp()),
            product=FinancialProductEnum.CREDIT_CARD.value,
            account_id=expense_account,
            classification_id=personel_class,
            subcategory_id=subcategory_list[idx],
        )

        trans_table: TransactionTable = TransactionTable(**new_transaction.model_dump())

        trans_table.id = idx
        trans_table.subcategory = SubCategoryTable()
        trans_table.subcategory.name = "Loyer"
        trans_table.subcategory.category = CategoryTable()
        trans_table.subcategory.category.name = category_list[idx]
        trans_table.subcategory.category.account_id = expense_account

        trans_table_list.append(trans_table)

    trans_table_sequence: Sequence[TransactionTable] = trans_table_list

    return trans_table_sequence


@fixture
def subcategory_list_from_database():

    subcat_table: SubCategoryTable
    subcat_bm: CreateSubCategory
    subcat_table_list: list[SubCategoryTable] = []

    name_list: list[str] = ["Loyer", "Essence", "Assurance Auto"]
    cat_list: list[str] = ["Habitation", "Transport", "Transport"]

    for idx, name in enumerate(name_list):
        subcat_bm = CreateSubCategory(name=name, category_id=1)

        subcat_table = SubCategoryTable(**subcat_bm.model_dump())

        subcat_table.id = idx + 1
        subcat_table.category = CategoryTable()
        subcat_table.category.name = cat_list[idx]

        subcat_table_list.append(subcat_table)

    return subcat_table_list


@fixture
def classification_list_from_database():

    class_table: ClassificationTable
    class_bm: CreateClassify
    class_table_list: list[ClassificationTable] = []

    name_list: list[str] = ["Personnal", "Familiy", "Couple"]

    for idx, name in enumerate(name_list):
        class_bm = CreateClassify(name=name)

        class_table = ClassificationTable(**class_bm.model_dump())

        class_table.id = idx + 1
        class_table_list.append(class_table)

    return class_table_list


@fixture
def database_url() -> str:
    return "sqlite:///C:/Users/user_name/AppData/Local/Financial_Advisor_for_Me/users/b5d49fb06b704b55bc4a9188b972ed78/db/user_database.db"


@fixture
def user_login():
    email: str = "Walker"
    password: str = "123456789"

    return email, password


@fixture
def user_signup(user_login):
    return user_login
