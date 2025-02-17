from typing import Any

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime as dt


class BaseUser(BaseModel):
    """
    Base user schema.
    """

    username: str = Field(
        description="User's username field. At least 3 characters in length and lower then 32.",
        min_length=3,
        max_length=32,
    )
    email: EmailStr = Field(
        description="Email field with validation. At least 6 characters in length and lower then 64.",
        max_length=64,
        min_length=6,
    )


class UserCreate(BaseUser):
    """
    User create schema.
    """

    pass


class UserUpdate(BaseUser):
    """
    User update schema.
    """

    username: str | None = Field(  # type: ignore[assignment]
        description="User's username field. At least 3 characters in length and lower then 32.",
        min_length=3,
        max_length=32,
        default=None,
    )
    email: EmailStr | None = Field(  # type: ignore[assignment]
        description="Email field with validation. At least 6 characters in length and lower then 64.",
        max_length=64,
        min_length=6,
        default=None,
    )


class UserFromDB(BaseUser):
    """
    User schema from database.
    """

    id: int = Field(
        description="User's identification number.",
        ge=0,
    )
    registration_date: dt = Field(description="User's registration date.")

    model_config = ConfigDict(
        from_attributes=True,
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Return a dict with user's data with stringified timestamp
        :return: model attrs and values as dictionary.
        """
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            registration_date=self.registration_date.strftime(
                "%d/%m/%Y, %H:%M:%S"
            ),
        )
