from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class FirstBase(DeclarativeBase):
    pass


class User(FirstBase):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
