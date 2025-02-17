from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
import datetime as dt

from app.src.core import Base


class User(Base):  # type: ignore
    """
    User ORM model.

    Fields:
    id: user's identification number
    username: user's username
    email: user's email
    registration_date: user's registration date
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
    )
    registration_date: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now(dt.UTC)
    )
