class CSVHeader:
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

    def __init__(self) -> None:
        self._article_number: str = "Article no"
        self._carte_number: str = "Carte no"
        self._transaction_date: str = "Date de la transaction"
        self._date_registering_statement: str = "Date de l'inscription au relevé"
        self._transaction_amount: str = "Montant de la transaction"
        self._description: str = "Description"


class BMO:
    @property
    def csv_header(self):
        return self._csv_header

    def __init__(self) -> None:
        self._csv_header: CSVHeader = CSVHeader()


bmo: BMO = BMO()

if __name__ == "__main__":
    bmo: BMO = BMO()
