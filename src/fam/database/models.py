from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

AppBase = declarative_base()


class User(AppBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    database_id: Mapped[str] = mapped_column(nullable=False, unique=True)
