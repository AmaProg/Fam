from typing import Sequence
from sqlalchemy.orm import Session
import typer

from fam.command.utils import build_choice, show_choice
from fam.database.users import service
from fam.database.users.models import AccountNicknameTable, SubCategoryTable
from fam.utils import fprint


def get_subcategory_from_database(db: Session) -> None:

    db_subcategory: Sequence[SubCategoryTable] = service.subcategory.get_subcategories(
        db
    )

    if not db_subcategory:
        fprint("No subcategories found")
        raise typer.Abort()

    _, subcat_choice = build_choice(db_subcategory, "categogy")

    show_choice(subcat_choice)


def get_account_nickname_from_database(db: Session) -> None:

    db_nickname: Sequence[AccountNicknameTable] = (
        service.account_nickname.get_account_nickname(db)
    )

    if not db_nickname:
        fprint("No account nickname found")
        raise typer.Abort()

    _, nickname_choice = build_choice(db_nickname, "nickname")

    show_choice(nickname_choice)
