from datetime import datetime
from typing import Any
from pandas import DataFrame, Series
from fam.bank.bmo import BMO
from fam.bank.constants import BANK_INSTANCE_TYPE
from fam.bank.tangerine import Tangerine
from fam.database.users.schemas import CreateTransactionModel
from fam.enums import BankEnum, FinancialProductEnum, TransactionTypeEnum


class BankStatement:
    def __init__(self) -> None:
        pass

    def standardize_statement(
        self,
        bank_name: BankEnum,
        csv_data: DataFrame,
        product: FinancialProductEnum,
    ) -> list[CreateTransactionModel]:

        bank: dict[BankEnum, Any] = {
            BankEnum.BMO: self._standardize_bmo_statement,
            BankEnum.TANGERINE: self._standardize_tangerine_statement,
        }

        func = bank.get(bank_name, None)

        return func(
            csv_data,
            product,
        )

    def _standardize_bmo_statement(
        self,
        df: DataFrame,
        financial_product: FinancialProductEnum,
    ) -> list[CreateTransactionModel]:

        bmo = BMO()

        date_head, desc_head, amount_head, _ = self._get_header(bmo, financial_product)

        transaction_list = self._build_standard_statement(
            amount_head=amount_head,
            csv_data=df,
            date_head=date_head,
            desc_head=desc_head,
            financial_product=financial_product,
            bank=BankEnum.BMO,
        )

        return transaction_list

    def _standardize_tangerine_statement(
        self,
        df: DataFrame,
        financial_product: FinancialProductEnum,
    ) -> list[CreateTransactionModel]:

        tangerine = Tangerine()
        financial: list[FinancialProductEnum] = [
            FinancialProductEnum.SAVE_ACCOUNT,
            FinancialProductEnum.CHECKING_ACCOUNT,
        ]

        date_head, desc_head, amount_head, name_head = self._get_header(
            tangerine, financial_product
        )

        if financial_product in financial:
            df[desc_head] = df[desc_head].fillna("")
            df[name_head] = df[name_head].fillna("")
            df[desc_head] = df[desc_head].astype(str) + " " + df[name_head].astype(str)
            df[amount_head] = -df[amount_head]

        transactions_list: list[CreateTransactionModel] = (
            self._build_standard_statement(
                amount_head=amount_head,
                csv_data=df,
                date_head=date_head,
                desc_head=desc_head,
                financial_product=financial_product,
                bank=BankEnum.TANGERINE,
            )
        )

        return transactions_list

    def _build_standard_statement(
        self,
        csv_data: DataFrame,
        amount_head: str,
        date_head: str,
        financial_product: FinancialProductEnum,
        desc_head: str,
        bank: BankEnum,
    ) -> list[CreateTransactionModel]:

        transactions: list[CreateTransactionModel] = []

        for _, transaction in csv_data.iterrows():

            date_timestamp, transaction_amount, transaction_type, transaction_desc = (
                self._get_transaction_value(
                    transaction=transaction,
                    amount_head=amount_head,
                    date_head=date_head,
                    financial_product=financial_product,
                    desc_head=desc_head,
                    bank=bank,
                )
            )

            transaction_model = CreateTransactionModel(
                account_id=0,
                account_nickname_id=0,
                classification_id=0,
                subcategory_id=0,
                amount=abs(transaction_amount),
                bank_name="",
                date=date_timestamp,
                description=transaction_desc.strip(),
                hash="",
                product=financial_product.value,
                transaction_type=transaction_type,
            )

            transactions.append(transaction_model)

        return transactions

    def _get_header(
        self,
        bank: BANK_INSTANCE_TYPE,
        financial_product: FinancialProductEnum,
    ) -> tuple[str, str, str, str]:
        date_head: str = bank.get_transaction_date(financial_product)
        desc_head: str = bank.get_description(financial_product)
        amount_head: str = bank.get_transaction_amount(financial_product)
        name_head: str = bank.get_name(financial_product)

        return date_head, desc_head, amount_head, name_head

    def _get_transaction_value(
        self,
        transaction: dict[str, Any],
        date_head: str,
        amount_head: str,
        desc_head: str,
        financial_product: FinancialProductEnum,
        bank: BankEnum,
    ) -> tuple[int, float, str, str]:

        transaction_date: str = str(transaction[date_head])
        amount: float = transaction[amount_head]
        transaction_type: str = self._define_transaction_type(
            amount=amount,
            product=financial_product,
        )
        date_timestamp: int = self._date_to_timestamp_by_bank(
            transaction_date,
            bank,
        )
        transaction_desc: str = transaction[desc_head]

        return date_timestamp, amount, transaction_type, transaction_desc

    def _date_to_timestamp_by_bank(self, date_str: str, bank: BankEnum) -> int:
        """
        Converts a date string to a Unix timestamp based on the bank.

        :param date_str: Date string
        :param bank: Bank enum
        :return: Unix timestamp corresponding to the date, or 0 if the date is invalid
        """
        # Define format strings for each bank
        FORMAT_STRINGS: dict[BankEnum, str] = {
            BankEnum.BMO: "%Y%m%d",
            BankEnum.TANGERINE: "%m/%d/%Y",
        }

        format_str = FORMAT_STRINGS.get(bank)

        if format_str is None:
            raise ValueError(f"Unsupported bank: {bank}")

        try:
            date_obj = datetime.strptime(date_str, format_str)
        except ValueError:
            return 0  # Or handle invalid date string as needed

        return int(date_obj.timestamp())

    def _define_transaction_type(
        self, amount: float, product: FinancialProductEnum
    ) -> str:

        negatif_amount: dict[FinancialProductEnum, str] = {
            FinancialProductEnum.CREDIT_CARD: TransactionTypeEnum.CREDIT.value,
            FinancialProductEnum.CHECKING_ACCOUNT: TransactionTypeEnum.CREDIT.value,
            FinancialProductEnum.SAVE_ACCOUNT: TransactionTypeEnum.CREDIT.value,
        }

        positif_amount: dict[FinancialProductEnum, str] = {
            FinancialProductEnum.CREDIT_CARD: TransactionTypeEnum.DEBIT.value,
            FinancialProductEnum.CHECKING_ACCOUNT: TransactionTypeEnum.DEBIT.value,
            FinancialProductEnum.SAVE_ACCOUNT: TransactionTypeEnum.DEBIT.value,
        }

        if amount > 0:
            transaction_type: str = positif_amount.get(product, "")
        else:
            transaction_type: str = negatif_amount.get(product, "")

        return transaction_type
