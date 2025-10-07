from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from clickhouse_sqlalchemy import engines


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    __table_args__ = (engines.MergeTree(order_by="id"),)
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None] = mapped_column(String(30))
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Address(Base):
    __tablename__ = "address"
    __table_args__ = (engines.MergeTree(order_by="id"),)
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
