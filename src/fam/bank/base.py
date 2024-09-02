class CreditCard:
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
