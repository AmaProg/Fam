from fam.bank.base import CheckAccount, CreditCard, FinancialInstitution

credit_card: CreditCard = CreditCard(
    article_number="Article no",
    carte_number="Carte no",
    date_registering_statement="Date de l'inscription au relevé",
    description="Description",
    transaction_amount="Montant de la transaction",
    transaction_date="Date de la transaction",
)

check_account: CheckAccount = CheckAccount(
    maxi_card="Maxi-Carte",
    transaction_type="Type de transaction",
    registration_date="Date d'inscription",
    amount=" Montant de la transaction",
    description="Description",
    name="",
)


class BMO(FinancialInstitution):
    def __init__(self) -> None:
        super().__init__()
        self._credit_card = credit_card
        self._check_account = check_account


if __name__ == "__main__":
    bmo: BMO = BMO()
