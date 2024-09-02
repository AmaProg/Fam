from fam.bank.base import CreditCard, FinancialInstitution

credit_card: CreditCard = CreditCard(
    article_number="",
    carte_number="",
    date_registering_statement="",
    description="Description",
    transaction_amount="Montant",
    transaction_date="Date de l'opération",
)


class Tangerine(FinancialInstitution):
    @property
    def credit_card(self):
        super().__init__
        self._credit_card = credit_card

    def __init__(self) -> None:
        self._credit_card: CreditCard = CreditCard(
            article_number="",
            carte_number="",
            date_registering_statement="",
            description="Description",
            transaction_amount="Montant",
            transaction_date="Date de l'opération",
        )
