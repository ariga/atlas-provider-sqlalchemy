from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# Importing by module name gives SecondBase a second copy.
from tests.testdata.multi_base.sessions import SecondBase


class Token(SecondBase):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"))
