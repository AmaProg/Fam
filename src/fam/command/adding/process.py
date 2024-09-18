# import typing_extensions
# from copy import copy
# from pathlib import Path
# from tkinter import filedialog
# from typing import Any
# from pandas import DataFrame
# from sqlalchemy.orm import Session
# import typer
# import pandas as pd

# from fam.bank.statement import BankStatement
# from fam.command.adding.validation import (
#     is_transaction_auto_classifiable,
#     matches_transaction_rule,
# )
# from fam.command.utils import (
#     date_to_timestamp_by_bank,
#     inverse_amount_sign_by_bank,
#     prompt_choice,
#     generate_transaction_hash,
# )
# from fam.database.users.models import (
#     T,
#     SubCategoryTable,
#     TransactionTable,
# )
# from fam.database.users.schemas import CreateTransactionModel
# from fam.enums import (
#     BankEnum,
#     FinancialProductEnum,
#     TransactionTypeEnum,
#     FinancialProductEnum,
# )
# from fam.database.users import service
# from fam.os.file import File
# from fam.utils import fprint, get_user_dir_from_database_url
# from fam.bank import constants as kbank


# def extract_transaction_details(
#     transaction: dict,
#     institution: kbank.BANK_INSTANCE_TYPE,
#     financial_product: FinancialProductEnum,
# ) -> tuple[str, float, str]:
#     """
#     Extrait les détails de la transaction en utilisant les méthodes de l'institution financière.

#     :param transaction: Dictionnaire représentant une transaction.
#     :param institution: Instance de la classe FinancialInstitution.
#     :param financial_product: Nom du produit financier.
#     :return: Un tuple contenant la description, le montant de la transaction et la date de la transaction et le hash.
#     """
#     desc_head: str = institution.get_description(financial_product)
#     amount_head: str = institution.get_transaction_amount(financial_product)
#     date_head: str = institution.get_transaction_date(financial_product)

#     description: str = transaction[desc_head]
#     transaction_amount: float = transaction[amount_head]
#     transaction_date: str = transaction[date_head]

#     return description, transaction_amount, transaction_date


# @typing_extensions.deprecated("")
# def open_dialog_file(bank: str) -> str:
#     csv_filename: str = filedialog.askopenfilename(
#         title=f"select the statement for the {bank} bank",
#         filetypes=(("CSV files", "*.csv"),),
#     )

#     return csv_filename


# @typing_extensions.deprecated("")
# def read_csv_by_bank(filename: str, bank: BankEnum) -> pd.DataFrame | None:
#     # Dictionnaire de configurations spécifiques pour chaque banque
#     bank_configurations = {
#         BankEnum.BMO: {"skiprows": 1},
#         BankEnum.TANGERINE: {"encoding": "ISO-8859-1"},
#         # Ajoutez d'autres banques et configurations ici si nécessaire
#     }

#     # Récupérer la configuration pour la banque spécifiée
#     config = bank_configurations.get(
#         bank, {"skiprows": 1}
#     )  # Valeur par défaut si la banque n'est pas trouvée

#     try:
#         # Lire le fichier CSV avec la configuration spécifique
#         return pd.read_csv(filename, **config)
#     except Exception as e:
#         print(f"Error reading CSV file: {e}")
#         return None


# def get_transaction_rule_file(database_url: str) -> Path:
#     user_folder: Path = get_user_dir_from_database_url(database_url)
#     trans_file: Path = user_folder / "transaction_rule.yaml"

#     return trans_file


# def add_transaction_to_rule_file(
#     database_url: str,
#     trans_base_model: CreateTransactionModel,
# ) -> None:
#     try:
#         trans_file: Path = get_transaction_rule_file(database_url)

#         content: dict[str, Any] = File.read_yaml_file(trans_file.as_posix()) or {}

#         data_rule_list: list[dict[str, Any]] = content.get("rule", [])

#         data_rule_list.append(trans_base_model.model_dump())

#         File.save_yaml_file(trans_file.as_posix(), {"rule": data_rule_list})

#     except Exception as e:
#         print(f"An error occurred: {e}")


# def classify_transaction_manually(
#     transaction: CreateTransactionModel,
#     subcat_choice: list[str],
#     class_choice: list[str],
#     subcat_dict: dict[int, SubCategoryTable],
#     database_url: str,
# ) -> CreateTransactionModel | None:

#     # description, transaction_amount, transaction_date = extract_transaction_details(
#     #     financial_product=financial_product,
#     #     institution=institution,
#     #     transaction=transaction,
#     # )

#     # show the message to select a subcategory.
#     subcat_id: int = prompt_choice(
#         subcat_choice,
#         "Select a category",
#         transaction.description,
#     )

#     if not subcat_id:
#         return None

#     # show the message to select a classification.
#     cls_id: int = prompt_choice(
#         class_choice,
#         "Select a category",
#         transaction.description,
#     )


#     subcategory_table: SubCategoryTable = subcat_dict.get(subcat_id, None)

#     if not subcategory_table:
#         raise typer.Abort()

#     transaction.subcategory_id = subcat_id
#     transaction.classification_id = cls_id
#     transaction.account_id = subcategory_table.category.account_id

#     # new_transaction: CreateTransactionModel = create_new_transaction(
#     #     transaction_hash=hash_id,
#     #     desc=description,
#     #     bank=bank,
#     #     financial_product=financial_product,
#     #     transaction_amount=transaction_amount,
#     #     transaction_date=transaction_date,
#     #     subcategory_id=subcat_id,
#     #     classification_id=cls_id,
#     #     account_id=subcategory_table.category.account_id,
#     #     nickname_id=nickname_id,
#     # )

#     # trans_table: TransactionTable | None = (
#     #     user_services.get_transaction_by_date_desc_bank(
#     #         db=db,
#     #         date=new_transaction.date,
#     #         desc=new_transaction.description,
#     #         bank=bank,
#     #     )
#     # )

#     # if trans_table is not None:
#     #     if typer.confirm(
#     #         text=f"The following description {new_transaction.description} already exists. Do you want to replace it?"
#     #     ):
#     #         user_services.update_transaction_by_desc(
#     #             db, new_transaction.description, new_transaction
#     #         )
#     #         return None
#     #     else:
#     #         return None

#     # Ask the user if they want to classify the transaction automatically
#     # for next time.
#     if typer.confirm(
#         "Do you want the next time you see the transaction to be filed automatically?"
#     ):
#         add_transaction_to_rule_file(
#             database_url=database_url,
#             trans_base_model=transaction,
#         )
#         fprint("The transaction has been successfully classified.")

#     return transaction


# def get_transaction_from_rules_file(
#     database_url: str,
#     trans_desc: str,
#     product: FinancialProductEnum,
#     bank: BankEnum,
#     nickname_id: int,
# ) -> CreateTransactionModel | None:

#     trans_file: Path = get_transaction_rule_file(database_url)

#     content: dict[str, list[dict[str, Any]]] = (
#         File.read_yaml_file(trans_file.as_posix()) or {}
#     )

#     rules: list[dict[str, Any]] = content.get("rule", [])

#     trans_base_model: CreateTransactionModel | None = matches_transaction_rule(
#         bank=bank.value,
#         product=product.value,
#         transaction_desc=trans_desc,
#         rules=rules,
#         nickname_id=nickname_id,
#     )

#     return trans_base_model


# def classify_transaction_auto(
#     transaction: CreateTransactionModel,
#     bank: BankEnum,
#     database_url: str,
#     financial_product: FinancialProductEnum,
#     nickname_id: int,
# ) -> CreateTransactionModel | None:

#     # description, transaction_amount, transaction_date = extract_transaction_details(
#     #     financial_product=financial_product,
#     #     institution=institution,
#     #     transaction=transaction,
#     # )

#     old_transaction: CreateTransactionModel | None = get_transaction_from_rules_file(
#         product=financial_product,
#         bank=bank,
#         database_url=database_url,
#         trans_desc=transaction.description,
#         nickname_id=nickname_id,
#     )

#     if old_transaction is None:
#         return None

#     transaction.description = old_transaction.description
#     transaction.classification_id = old_transaction.classification_id
#     transaction.account_id = old_transaction.account_id
#     transaction.subcategory_id = old_transaction.subcategory_id

#     transaction_classified = transaction

#     # transaction_classified = create_new_transaction(
#     #     transaction_hash=hash_id,
#     #     desc=old_transaction.description,
#     #     financial_product=financial_product,
#     #     transaction_amount=transaction.amount,
#     #     transaction_date=transaction.date,
#     #     bank=bank,
#     #     classification_id=old_transaction.classification_id,
#     #     subcategory_id=old_transaction.subcategory_id,
#     #     account_id=old_transaction.account_id,
#     #     nickname_id=nickname_id,
#     # )

#     return transaction_classified


# def define_transaction_type(amount: float, product: FinancialProductEnum) -> str:

#     negatif_amount: dict[FinancialProductEnum, str] = {
#         FinancialProductEnum.CREDIT_CARD: TransactionTypeEnum.CREDIT.value,
#         FinancialProductEnum.CHECKING_ACCOUNT: TransactionTypeEnum.CREDIT.value,
#         FinancialProductEnum.SAVE_ACCOUNT: TransactionTypeEnum.CREDIT.value,
#     }

#     positif_amount: dict[FinancialProductEnum, str] = {
#         FinancialProductEnum.CREDIT_CARD: TransactionTypeEnum.DEBIT.value,
#         FinancialProductEnum.CHECKING_ACCOUNT: TransactionTypeEnum.DEBIT.value,
#         FinancialProductEnum.SAVE_ACCOUNT: TransactionTypeEnum.DEBIT.value,
#     }

#     if amount > 0:
#         transaction_type: str = positif_amount.get(product, "")
#     else:
#         transaction_type: str = negatif_amount.get(product, "")

#     return transaction_type


# @typing_extensions.deprecated("Use categorize_transaction fucntion")
# def classify_transactions(
#     df: DataFrame,
#     subcat_choice: list[str],
#     class_choice: list[str],
#     subcat_dict: dict[int, SubCategoryTable],
#     product: FinancialProductEnum,
#     bank: BankEnum,
#     db: Session,
#     database_url: str,
#     nickname_id: int,
# ) -> list[TransactionTable]:

#     transactions: list[TransactionTable] = []
#     bank_ins: kbank.BANK_INSTANCE_TYPE = kbank.BANK_INST[bank]
#     desc_head: str = bank_ins.get_description(product)
#     amount_head: str = bank_ins.get_transaction_amount(product)
#     date_head: str = bank_ins.get_transaction_date(product)
#     name_head: str = bank_ins.get_name(product)

#     if bank == BankEnum.TANGERINE:
#         df[desc_head] = df[desc_head].fillna("")
#         df[name_head] = df[name_head].fillna("")
#         df[desc_head] = df[desc_head].astype(str) + "_" + df[name_head].astype(str)

#     df_csv = inverse_amount_sign_by_bank(
#         df=df,
#         bank=bank,
#         financial_product=product,
#         institution=bank_ins,
#     )

#     for _, trans in df_csv.iterrows():

#         transaction_hash: str = generate_transaction_hash(
#             amount_value=trans[amount_head],
#             bank_name=bank.value,
#             date_value=date_to_timestamp_by_bank(str(trans[date_head]), bank),
#             desc=trans[desc_head],
#             nickname_id=nickname_id,
#             product_name=product.value,
#         )

#         db_transaction: TransactionTable = service.transaction.get_transaction_by_hash(
#             db=db,
#             hash=transaction_hash,
#         )

#         if db_transaction is not None:
#             fprint(f"The following description {trans[desc_head]} already exists.")
#             continue

#         if is_transaction_auto_classifiable(
#             database_url=database_url,
#             trans_desc=trans[desc_head],
#             product=product,
#             bank=bank,
#             nickname_id=nickname_id,
#         ):
#             new_transaction: CreateTransactionModel | None = classify_transaction_auto(
#                 transaction=trans.to_dict(),
#                 institution=bank_ins,
#                 bank=bank,
#                 database_url=database_url,
#                 financial_product=product,
#                 hash_id=transaction_hash,
#                 nickname_id=nickname_id,
#             )

#             if new_transaction is not None:
#                 transactions.append(
#                     TransactionTable(**copy(new_transaction.model_dump()))
#                 )
#                 fprint(
#                     f"Transaction {trans[desc_head]} has been automatically classified."
#                 )
#                 continue
#             else:
#                 fprint("The transaction could not be automatically classified.")

#         new_transaction: CreateTransactionModel | None = classify_transaction_manually(
#             db=db,
#             bank=bank,
#             institution=bank_ins,
#             class_choice=class_choice,
#             database_url=database_url,
#             transaction=trans.to_dict(),
#             financial_product=product,
#             subcat_choice=subcat_choice,
#             subcat_dict=subcat_dict,
#             hash_id=transaction_hash,
#             nickname_id=nickname_id,
#         )

#         if new_transaction is None:
#             continue

#         transactions.append(TransactionTable(**copy(new_transaction.model_dump())))

#     return transactions


# def categorize_transaction(
#     bank: BankEnum,
#     df: DataFrame,
#     product: FinancialProductEnum,
#     nickname_id: int,
#     db: Session,
#     database_url: str,
#     subcat_choice: list[str],
#     class_choice: list[str],
#     subcat_dict: dict[int, SubCategoryTable],
# ) -> list[TransactionTable]:

#     bank_statement = BankStatement()

#     transaction_list = bank_statement.standardize_statement(
#         bank_name=bank,
#         csv_data=df,
#         product=product,
#     )

#     transactions_table: list[TransactionTable] = []

#     for transaction in transaction_list:

#         transaction.bank_name = bank.value
#         transaction.account_nickname_id = nickname_id

#         # hash_id: str = generate_transaction_hash(
#         #     amount_value=transaction.amount,
#         #     bank_name=transaction.bank_name,
#         #     date_value=transaction.date,
#         #     desc=transaction.description,
#         #     nickname_id=transaction.account_nickname_id,
#         #     product_name=transaction.product,
#         # )

#         hash_id: str = ""

#         transaction.hash = hash_id

#         # Get transaction by hash_id to check if already exist in the database

#         db_transaction: TransactionTable = service.transaction.get_transaction_by_hash(
#             db=db,
#             hash=hash_id,
#         )

#         if db_transaction is not None:
#             fprint(
#                 f"The following description {transaction.description} already exists."
#             )
#             continue

#         result: bool = is_transaction_auto_classifiable(
#             bank=bank,
#             database_url=database_url,
#             nickname_id=nickname_id,
#             product=product,
#             trans_desc=transaction.description,
#         )

#         if db_transaction

#             new_transaction: CreateTransactionModel | None = classify_transaction_auto(
#                 database_url=database_url,
#                 bank=bank,
#                 financial_product=product,
#                 nickname_id=nickname_id,
#                 transaction=transaction,
#             )

#             if new_transaction:
#                 transactions_table.append(
#                     TransactionTable(**new_transaction.model_dump())
#                 )
#                 fprint(
#                     f"Transaction {transaction.description} has been automatically classified."
#                 )
#                 continue
#             else:
#                 fprint("The transaction could not be automatically classified.")

#             continue

#         new_transaction: CreateTransactionModel | None = classify_transaction_manually(
#             class_choice=class_choice,
#             database_url=database_url,
#             transaction=transaction,
#             subcat_choice=subcat_choice,
#             subcat_dict=subcat_dict,
#         )
#         if new_transaction is None:
#             continue

#         transactions_table.append(TransactionTable(**new_transaction.model_dump()))

#     return transactions_table


# def create_new_transaction(
#     transaction_hash: str,
#     desc: str,
#     financial_product: FinancialProductEnum,
#     transaction_amount: float,
#     transaction_date: int,
#     classification_id: int,
#     subcategory_id: int,
#     account_id: int,
#     bank: BankEnum,
#     nickname_id: int,
# ) -> CreateTransactionModel:
#     transaction_model: CreateTransactionModel = CreateTransactionModel(
#         hash=transaction_hash,
#         description=desc.strip(),
#         product=financial_product.value,
#         amount=abs(transaction_amount),
#         date=transaction_date,
#         bank_name=bank.value,
#         classification_id=classification_id,
#         subcategory_id=subcategory_id,
#         account_id=account_id,
#         transaction_type=define_transaction_type(transaction_amount, financial_product),
#         account_nickname_id=nickname_id,
#     )

#     return transaction_model
