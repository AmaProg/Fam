from sqlalchemy.orm import Session

from fam.database.users import service


def delete_all_transaction(db: Session) -> None:

    service.transaction.delete_all_transaction(db)
