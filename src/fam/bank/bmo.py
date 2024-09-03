from fam.bank.base import CreditCard, FinancialInstitution

credit_card: CreditCard = CreditCard(
    article_number="Article no",
    carte_number="Carte no",
    date_registering_statement="Date de l'inscription au relevé",
    description="Description",
    transaction_amount="Montant de la transaction",
    transaction_date="Date de la transaction",
)


class BMO(FinancialInstitution):
    def __init__(self) -> None:
        super().__init__()
        self._credit_card = credit_card


if __name__ == "__main__":
    bmo: BMO = BMO()
