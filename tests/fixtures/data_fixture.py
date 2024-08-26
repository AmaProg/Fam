from io import StringIO
import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    # Données CSV en tant que chaîne de caractères
    csv_data = """Article no,Carte no,Date de la transaction,Date de l'inscription au relevé,Montant de la transaction,Description
1,12345,20240801,20240801,100.00,Description 1
2,67890,20240802,20240802,200.00,IGA Epicerie
3,54321,20240803,20240803,300.00,Description 3
"""

    # Utiliser StringIO pour simuler un fichier CSV
    csv_file = StringIO(csv_data)

    # Lire les données CSV dans un DataFrame
    df = pd.read_csv(csv_file)

    return df
