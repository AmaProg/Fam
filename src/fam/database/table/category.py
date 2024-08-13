from pathlib import Path
from typing import Any
from enum import Enum

import typer
from fam.cli import app_cli

from fam.system.file import File
from fam.utils import fprint

NAME = "name"
DESC = "description"


class Category:
    def __init__(self, filename: str) -> None:
        self._filename: str = filename
        self._data: dict[str, Any] = self._load_table()

    def insert_data(self, cat_name: str, cat_desc: str, cat_section: str) -> None:
        cat_data: dict[str, Any] = {"name": cat_name, "description": cat_desc}

        section: list[dict[str, Any]] | None = self._get_category_section(cat_section)

        if section is None:
            section = []

            self._add_data(section, cat_data, cat_section)

            # section.append(cat_data)

            # self._data["category"][cat_section] = section

        else:

            if self._is_category_exist(section, cat_name):
                raise ValueError(f"The category {cat_name} exist")

            self._add_data(section, cat_data, cat_section)

    def _add_data(
        self,
        section: list[dict[str, Any]],
        cat_data: dict[str, Any],
        cat_section: str,
    ) -> None:
        section.append(cat_data)

        self._data["category"][cat_section] = section

    def _is_category_exist(self, section: list[dict[str, Any]], cat_name: str) -> bool:

        for idx, cat in enumerate(section):
            if cat[NAME] == cat_name:
                return True

        return False

    def submit(self) -> None:
        File.save_file(self._filename, self._data, "yaml")

    def _load_table(self) -> dict[str, Any]:
        data = File.read_file(self._filename, "yaml")

        return data if data is not None else {}

    def _get_category_section(self, cat_section: str) -> list[dict[str, Any]] | None:
        section: list[dict[str, Any]] = self._data["category"][cat_section]

        return section

    # def __init__(self, filename: str) -> None:
    #     self._filename: str = filename
    #     self._data_table: dict[str, Any] = {}
    #     self._data_row: list[dict[str, Any]] | None = self._get_table()
    #     self._data_section: dict[str, list[dict[str, Any]]] = {}

    # def add_data(self, name: str, desc: str, section_category: str) -> None:

    #     section: dict[str, list[dict[str, Any]]] | None = self._get_section(
    #         section_category
    #     )
    #     data = {"name": name, "description": desc}

    #     if section is None:
    #         new_section: dict[str, list[dict[str, Any]]] = {}

    #         new_section[section_category] = [data]

    #         self._data_section = new_section

    #     else:

    #         section: dict[str, list[dict[str, Any]]] = self._get_section(
    #             section_category
    #         )

    #         # if section is not None:
    #         #     self._data_section = section[section_category]

    #         # if self._name_exist(name, self._data_section):
    #         #     fprint(
    #         #         f"The category '[yellow]{name}[/yellow]' already exists for the '[yellow]{section_category}[/yellow]' section"
    #         #     )
    #         #     raise typer.Abort()

    #         # data = {
    #         #     "name": name,
    #         #     "description": desc,
    #         # }

    #         # data_header = {}
    #         # data_header[section_category] = [data]

    #         # self._data_section.append(data_header)

    # def submit(self) -> None:

    #     self._data_table["category"] = self._data_section

    #     File.save_file(self._filename, self._data_table, "yaml")

    # def _get_table(self) -> list[dict[str, Any]]:
    #     self._data_table = File.read_file(self._filename, "yaml")

    #     return self._data_table["category"]

    # def _name_exist(self, name: str, data_list: list) -> bool:

    #     if len(data_list) == 0:
    #         return False

    #     for idx, value in enumerate(data_list):
    #         pass

    # def _get_section(self, section: str) -> dict[str, list[dict[str, Any]]] | None:

    #     if self._data_row is None:
    #         return None

    #     for idx, value in enumerate(self._data_row):
    #         if section in value.keys():
    #             return self._data_row[idx]
    #         else:
    #             return None
