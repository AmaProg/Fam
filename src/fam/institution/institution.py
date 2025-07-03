from fam.institution.account import CheckAccount, SaveAccount, CreditCard


class Tangerine:

    save_account: SaveAccount = SaveAccount(
        amount="Montant",
        description="Nom",
        registration_date="Date",
        transaction_type="Transaction",
        name="Description",
    )
    check_account: CheckAccount = CheckAccount(
        header_amount="Montant",
        header_description="Nom",
        header_registration_date="Date",
        header_transaction_type="Transaction",
        header_name="Description",
    )
    credit_card_account: CreditCard = CreditCard(
        description="Nom",
        amount="Montant",
        transaction_date="Date de l'opération",
    )


class BMO:
    credit_card_account: CreditCard = CreditCard(
        article_number="Article no",
        carte_number="Carte no",
        date_registering_statement="Date de l'inscription au relevé",
        description="Description",
        amount="Montant de la transaction",
        transaction_date="Date de la transaction",
        sign_reversed=True,
    )

    check_account: CheckAccount = CheckAccount(
        header_maxi_card="Maxi-Carte",
        header_transaction_type="Type de transaction",
        header_registration_date="Date d'inscription",
        header_amount="Montant de la transaction",
        header_description="Description",
    )

    save_account: SaveAccount = SaveAccount(
        maxi_card="Maxi-Carte",
        transaction_type="Type de transaction",
        registration_date="Date d'inscription",
        amount="Montant de la transaction",
        description="Description",
    )


class Desjardin:
    credit_card_account: CreditCard = CreditCard(
        description="Nom",
        amount="Montant",
        transaction_date="Date de l'opération",
    )

    check_account: CheckAccount = CheckAccount(
        header_amount="Montant",
        header_description="Nom",
        header_registration_date="Date",
        header_transaction_type="Transaction",
        header_name="Description",
    )

    save_account: SaveAccount = SaveAccount(
        amount="Montant",
        description="Nom",
        registration_date="Date",
        transaction_type="Transaction",
        name="Description",
    )
