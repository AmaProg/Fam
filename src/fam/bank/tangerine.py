from fam.bank.base import CheckAccount, CreditCard, FinancialInstitution

credit_card: CreditCard = CreditCard(
    article_number="",
    carte_number="",
    date_registering_statement="",
    description="Nom",
    transaction_amount="Montant",
    transaction_date="Date de l'opération",
)

check_account: CheckAccount = CheckAccount(
    amount="Montant",
    description="Nom",
    maxi_card="",
    registration_date="Date",
    transaction_type="Transaction",
    name="Description",
)


class Tangerine(FinancialInstitution):

    def __init__(self) -> None:
        super().__init__()
        self._credit_card = credit_card
        self._check_account = check_account
