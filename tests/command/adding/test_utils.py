from typing import Sequence
from fam.command.utils import build_choice
from fam.database.users.models import CategoryTable, SubCategoryTable
from fam.database.users.schemas import CreateSubCategory


def test_build_choice_for_category():

    name_list: list[str] = ["Essence", "Loyer"]
    category_list: list[str] = ["Transport", "Habitation"]
    subcatBM: CreateSubCategory
    sub_table: SubCategoryTable
    sub_table_list: list[SubCategoryTable] = []

    for idx, name in enumerate(name_list):

        subcatBM = CreateSubCategory(name=name, category_id=1)

        sub_table = SubCategoryTable(**subcatBM.model_dump())

        sub_table.id = idx + 1
        sub_table.category = CategoryTable()
        sub_table.category.name = category_list[idx]

        sub_table_list.append(sub_table)

    item_dict, item_choice = build_choice(sub_table_list, "categogy")

    assert "1: essence [yellow](Transport)[/yellow]".lower() in item_choice
