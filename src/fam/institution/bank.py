import copy
from datetime import datetime
from pandas import DataFrame

from fam.enums import BankEnum, TransactionTypeEnum, FinancialProductEnum
from fam.institution.institution import Tangerine, BMO, Desjardin
from fam.institution.account import CheckAccount, SaveAccount, CreditCard
from fam.institution.enums import AccountTypeEnum
from fam.database.users.schemas import CreateTransactionModel


class Bank:
    @property
    def name(self) -> str:
        return self._bank_name.value

    def __init__(self, bank_name: BankEnum) -> None:
        self._bank_name: BankEnum = bank_name
        self._save_account: SaveAccount
        self._check_account: CheckAccount
        self._credit_card_account: CreditCard

        self._create_account()

    # ===== public methode =====
    def read_statement(self, account_type: FinancialProductEnum, statement: DataFrame):

        statement.columns = (
            statement.columns.str.strip()
        )  # remove espace before and after

        transaction_list: list[CreateTransactionModel] = []

        if account_type == FinancialProductEnum.CHECKING_ACCOUNT:

            transaction_list = self._get_transaction_by_check_account_statement(
                account_type=account_type,
                statement=statement,
            )

        elif account_type == FinancialProductEnum.SAVE_ACCOUNT:

            transaction_list = self._get_transaction_by_save_account_statement(
                account_type=account_type,
                statement=statement,
            )

        elif account_type == FinancialProductEnum.CREDIT_CARD:

            transaction_list = self._get_transaction_by_credit_card_account_statement(
                account_type=account_type,
                statement=statement,
            )

        else:
            return transaction_list

        return transaction_list

    # ===== end public methode =====
    def _get_transaction_type(self, amount: float, sign_reversed: bool):
        """_summary_

        Args:
            amount (float): _description_
            sign_reversed (bool): _description_

        Returns:
            _type_: _description_
        >>> bank: Bank = Bank(bank_name=BankEnum.BMO)
        >>> bank._get_transaction_type(150.25, True)
        'debit'
        >>> bank: Bank = Bank(bank_name=BankEnum.BMO)
        >>> bank._get_transaction_type(-150.25, False)
        'debit'
        >>> bank: Bank = Bank(bank_name=BankEnum.BMO)
        >>> bank._get_transaction_type(-150.25, True)
        'credit'
        >>> bank: Bank = Bank(bank_name=BankEnum.BMO)
        >>> bank._get_transaction_type(150.25, False)
        'credit'
        """

        is_credit = (amount >= 0) != sign_reversed

        return (
            TransactionTypeEnum.CREDIT.value
            if is_credit
            else TransactionTypeEnum.DEBIT.value
        )

    def _create_new_transaction(
        self,
        amount: float,
        date: int,
        desc: str,
        product: FinancialProductEnum,
        transaction_type: str,
    ):
        new_transaction: CreateTransactionModel = CreateTransactionModel(
            account_id=0,
            account_nickname_id=0,
            amount=abs(amount),
            auto_categorize=False,
            bank_name=self._bank_name,
            classification_id=0,
            date=date,
            description=desc,
            hash="",
            payment_proportion=1,
            product=product.value,
            subcategory_id=0,
            transaction_type=transaction_type,
        )

        return new_transaction

    def _get_transaction_by_check_account_statement(
        self,
        account_type: FinancialProductEnum,
        statement: DataFrame,
    ):
        transaction_list: list[CreateTransactionModel] = []

        for _, transaction in statement.iterrows():

            transaction_amount: float = transaction[self._check_account.header_amount]
            transaction_date: int = self._date_to_timestamp_by_bank(
                bank=self._bank_name,
                date=transaction[self._check_account.header_registration_date],
            )
            transaction_description: str = transaction[
                self._check_account.header_description
            ]
            transaction_type: str = self._get_transaction_type(
                amount=transaction_amount,
                sign_reversed=self._check_account.sign_reversed,
            )

            new_transaction: CreateTransactionModel = self._create_new_transaction(
                amount=transaction_amount,
                date=transaction_date,
                desc=transaction_description,
                product=account_type,
                transaction_type=transaction_type,
            )

            transaction_list.append(copy.copy(new_transaction))

        return transaction_list

    def _get_transaction_by_save_account_statement(
        self,
        account_type: FinancialProductEnum,
        statement: DataFrame,
    ):
        transaction_list: list[CreateTransactionModel] = []

        for _, transaction in statement.iterrows():

            transaction_amount: float = transaction[self._save_account.amount]
            transaction_date: int = self._date_to_timestamp_by_bank(
                bank=self._bank_name,
                date=transaction[self._save_account.registration_date],
            )
            transaction_description: str = transaction[self._save_account.description]
            transaction_type: str = self._get_transaction_type(
                amount=transaction_amount,
                sign_reversed=self._save_account.sign_reversed,
            )

            new_transaction: CreateTransactionModel = self._create_new_transaction(
                amount=transaction_amount,
                date=transaction_date,
                desc=transaction_description,
                product=account_type,
                transaction_type=transaction_type,
            )

            transaction_list.append(copy.copy(new_transaction))

        return transaction_list

    def _get_transaction_by_credit_card_account_statement(
        self,
        account_type: FinancialProductEnum,
        statement: DataFrame,
    ):
        transaction_list: list[CreateTransactionModel] = []

        for _, transaction in statement.iterrows():

            transaction_amount: float = transaction[self._credit_card_account.amount]
            transaction_date: int = self._date_to_timestamp_by_bank(
                bank=self._bank_name,
                date=str(transaction[self._credit_card_account.transaction_date]),
            )
            transaction_description: str = transaction[
                self._credit_card_account.description
            ]
            transaction_type: str = self._get_transaction_type(
                amount=transaction_amount,
                sign_reversed=self._credit_card_account.sign_reversed,
            )

            new_transaction: CreateTransactionModel = self._create_new_transaction(
                amount=transaction_amount,
                date=transaction_date,
                desc=transaction_description,
                product=account_type,
                transaction_type=transaction_type,
            )

            transaction_list.append(copy.copy(new_transaction))

        return transaction_list

    def _create_account(self):
        bank_classes: dict[BankEnum, type] = {
            BankEnum.TANGERINE: Tangerine,
            BankEnum.BMO: BMO,
            BankEnum.DESJARDIN: Desjardin,
        }

        bank_class = bank_classes.get(self._bank_name)

        if bank_class:
            self._save_account = bank_class.save_account
            self._check_account = bank_class.check_account
            self._credit_card_account = bank_class.credit_card_account

    def _date_to_timestamp_by_bank(self, date: str, bank: BankEnum) -> int:
        """
        Converts a date string to a Unix timestamp based on the bank.

        :param date_str: Date string
        :param bank: Bank enum
        :return: Unix timestamp corresponding to the date, or 0 if the date is invalid
        """

        date = str(date)
        # Define format strings for each bank
        FORMAT_STRINGS: dict[BankEnum, str] = {
            BankEnum.BMO: "%Y%m%d",
            BankEnum.TANGERINE: "%m/%d/%Y",
            BankEnum.DESJARDIN: "%m/%d/%Y",
        }

        format_str = FORMAT_STRINGS.get(bank)

        if format_str is None:
            raise ValueError(f"Unsupported bank: {bank}")

        try:
            date_obj = datetime.strptime(date, format_str)
        except ValueError:
            return 0  # Or handle invalid date string as needed

        return int(date_obj.timestamp())


if __name__ == "__main__":

    import doctest

    doctest.testmod()

    data = {
        "Date d'inscription": ["20250404", "20250407", "20250411"],
        "Montant de la transaction": [237.61, -168.09, 234.85],
        "Description": ["Salaire", "assurance", "Uber"],
    }

    data2 = {
        "Date de la transaction": ["20250404", "20250407", "20250411"],
        "Montant de la transaction": [237.61, -168.09, 234.85],
        "Description": ["Salaire", "assurance", "Uber"],
    }

    df: DataFrame = DataFrame(data2)
    bank: Bank = Bank(bank_name=BankEnum.BMO)
    transations: list[CreateTransactionModel] = bank.read_statement(
        FinancialProductEnum.CREDIT_CARD, statement=df
    )

    print(bank.name)
    print(transations[1])
