from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class SecondBase(DeclarativeBase):
    pass


class Session(SecondBase):
    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
