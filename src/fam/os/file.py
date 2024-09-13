from pathlib import Path
from typing import Any, Literal
import tkinter as tk
from tkinter import filedialog

import pandas as pd
import yaml
from fam.enums import BankEnum
from fam.os import directory


class File:
    def __init__(self, dir: directory.Dir) -> None:
        self._directory: directory.Dir = dir

    def create_file(self, dir_path: str, filename: str) -> None:

        file: Path = Path(dir_path) / filename

        file.touch()

    @classmethod
    def read_file(cls, path: str, type_file: Literal["yaml"]):
        with open(path, "r") as f:

            if type_file == "yaml":
                return yaml.safe_load(f)
            else:
                return f

    @classmethod
    def read_yaml_file(cls, path: str) -> dict[str, Any] | None:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def save_yaml_file(cls, path: str, data: Any) -> None:
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)

    @classmethod
    def save_file(cls, path: str, data, type_file: Literal["yaml"]):
        with open(path, "w") as f:

            if type_file == "yaml":
                yaml.safe_dump(data, f)

    @classmethod
    def open_dialog(cls, bank: str) -> str:
        root = tk.Tk()
        root.withdraw()

        filename: str = filedialog.askopenfilename(
            title=f"Select the statement for the {bank} bank",
            filetypes=(("CSV files", "*.csv"),),
        )

        return filename

    @classmethod
    def read_csv_by_bank(cls, filename: str, bank: BankEnum) -> pd.DataFrame | None:
        # Dictionnaire de configurations spécifiques pour chaque banque
        bank_configurations = {
            BankEnum.BMO: {"skiprows": 1},
            BankEnum.TANGERINE: {"encoding": "ISO-8859-1"},
            # Ajoutez d'autres banques et configurations ici si nécessaire
        }

        # Récupérer la configuration pour la banque spécifiée
        config = bank_configurations.get(
            bank, {"skiprows": 1}
        )  # Valeur par défaut si la banque n'est pas trouvée

        try:
            # Lire le fichier CSV avec la configuration spécifique
            return pd.read_csv(filename, **config)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
