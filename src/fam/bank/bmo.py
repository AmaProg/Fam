from fam.bank.csv_herder import CSVHeader


class BMO(CSVHeader):
    def __init__(self) -> None:
        super().__init__()


bmo: BMO = BMO()

if __name__ == "__main__":
    bmo: BMO = BMO()
