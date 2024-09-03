from copy import copy
from fam.bank import csv_herder
from fam.enums import FinancialProductEnum


class CreditCard:
    @property
    def article_number(self):
        return self._article_number

    @property
    def carte_number(self):
        return self._carte_number

    @property
    def transaction_date(self):
        return self._transaction_date

    @property
    def date_registering_statement(self):
        return self._date_registering_statement

    @property
    def transaction_amount(self):
        return self._transaction_amount

    @property
    def description(self):
        return self._description

    def __init__(
        self,
        article_number: str,
        carte_number: str,
        transaction_date: str,
        date_registering_statement: str,
        transaction_amount: str,
        description: str,
    ) -> None:
        self._article_number: str = article_number
        self._carte_number: str = carte_number
        self._transaction_date: str = transaction_date
        self._date_registering_statement: str = date_registering_statement
        self._transaction_amount: str = transaction_amount
        self._description: str = description


class CheckAccount:
    def __init__(
        self,
        maxi_card: str,
        transaction_type: str,
        registration_date: str,
        amount: str,
        description: str,
    ) -> None:
        """
        Initialize a new Transaction instance.

        :param maxi_card: The maxi-card identifier.
        :param transaction_type: The type of the transaction.
        :param registration_date: The date the transaction was registered.
        :param amount: The amount of the transaction.
        :param description: Description of the transaction.
        """
        self.maxi_card: str = maxi_card
        self.transaction_type: str = transaction_type
        self.registration_date: str = registration_date
        self.amount: str = amount
        self.description: str = description

    def __str__(self) -> str:
        """
        Return a string representation of the Transaction.

        :return: A string describing the transaction.
        """
        return (
            f"Maxi-Card: {self.maxi_card}, "
            f"Transaction Type: {self.transaction_type}, "
            f"Registration Date: {self.registration_date}, "
            f"Amount: {self.amount}, "
            f"Description: {self.description}"
        )


class SaveAccount:
    def __init__(
        self,
        maxi_card: str,
        transaction_type: str,
        registration_date: str,
        amount: str,
        description: str,
    ) -> None:
        """
        Initialize a new Transaction instance.

        :param maxi_card: The maxi-card identifier.
        :param transaction_type: The type of the transaction.
        :param registration_date: The date the transaction was registered.
        :param amount: The amount of the transaction.
        :param description: Description of the transaction.
        """
        self.maxi_card: str = maxi_card
        self.transaction_type: str = transaction_type
        self.registration_date: str = registration_date
        self.amount: str = amount
        self.description: str = description

    def __str__(self) -> str:
        """
        Return a string representation of the Transaction.

        :return: A string describing the transaction.
        """
        return (
            f"Maxi-Card: {self.maxi_card}, "
            f"Transaction Type: {self.transaction_type}, "
            f"Registration Date: {self.registration_date}, "
            f"Amount: {self.amount}, "
            f"Description: {self.description}"
        )


class FinancialInstitution:
    def __init__(
        self,
    ) -> None:
        self._credit_card: CreditCard | None = None
        self._check_account: CheckAccount | None = None
        self._save_account: SaveAccount | None = None
        self._csv_header: dict[FinancialProductEnum, str] = {
            FinancialProductEnum.CREDIT_CARD: "None",
            FinancialProductEnum.CHECKING_ACCOUNT: "None",
        }

    def get_description(self, product: FinancialProductEnum) -> str:

        condition: list[str] = [
            self._credit_card.description if self._credit_card is not None else "s",
            self._check_account.description if self._check_account is not None else "d",
        ]

        csv_header_build = self._build_csv_header(condition)

        return csv_header_build.get(product, "No value")

    def get_transaction_date(self, product: FinancialProductEnum) -> str:

        condition: list[str] = [
            self._credit_card.transaction_date if self._credit_card else "",
            self._check_account.registration_date if self._check_account else "",
        ]

        csv_header_build = self._build_csv_header(condition)

        return csv_header_build.get(product, "No Value")

    def get_transaction_amount(self, product: FinancialProductEnum) -> str:

        condition: list[str] = [
            self._credit_card.transaction_amount if self._credit_card else "",
            self._check_account.amount if self._check_account else "",
        ]

        csv_header_build = self._build_csv_header(condition)

        return csv_header_build.get(product, "No Value")

    def _verify_lengths(self, condition: list, csv_header: dict) -> bool:
        """
        Vérifie si la longueur de la liste condition est égale à celle du dictionnaire csv_header.
        Lève une exception si les longueurs sont différentes.

        Args:
            condition (list): Liste de conditions.
            csv_header (dict): Dictionnaire contenant les clés à mettre à jour.

        Returns:
            bool: True si les longueurs sont égales.

        Raises:
            ValueError: Si les longueurs de condition et csv_header sont différentes.
        """
        if len(condition) != len(csv_header):
            raise ValueError(
                f"The lengths are different: condition = {len(condition)}, csv_header = {len(csv_header)}"
            )
        return True

    def _build_csv_header(self, condition: list[str]):

        self._verify_lengths(condition, self._csv_header)

        for idx, key in enumerate(self._csv_header.keys()):
            self._csv_header[key] = copy(condition[idx])

        return self._csv_header
