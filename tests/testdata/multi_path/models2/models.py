from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User2(Base):
    __tablename__ = "user_account2"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None] = mapped_column(String(30))
    addresses: Mapped[list["Address2"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Address2(Base):
    __tablename__ = "address2"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account2.id"))
    user: Mapped["User2"] = relationship(back_populates="addresses")
