from sqlalchemy import select, func
from datetime import (
    datetime as dt,
    timedelta as td,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy

from app.src.exceptions import UserNotFoundException
from app.src.models import User
from app.src.schemas.entities import UserUpdate, UserCreate
from app.src.schemas.query import UserPaginatorQueryParams


class UserRepository:
    """
    Repository class for User model.
    """

    def __init__(self, db: "SQLAlchemy") -> None:
        self._db = db

    def get_all(
        self,
        paginator_params: UserPaginatorQueryParams,
    ) -> list[User]:
        """
        Get all users with applied pagination params.
        :param paginator_params: pagination params schema
        :return: list of users
        """
        stmt = select(User).offset(paginator_params.offset)
        if paginator_params.limit != 0:
            stmt = stmt.limit(paginator_params.limit)
        result = list(self._db.session.scalars(stmt).all())
        return result

    def _get_user_by_field(self, field_name: str, value: str) -> User | None:
        """
        Get user by field. Service method.
        :param field_name: field name
        :param value: field value
        :return: user model if found else None
        """
        stmt = select(User).filter_by(**{field_name: value})
        result = self._db.session.scalars(stmt).one_or_none()
        return result

    def get_one(self, id: int) -> User:
        """
        Get user by id.
        :param id: user id
        :return: user
        """
        result = self._get_user_by_field("id", str(id))

        if result is None:
            raise UserNotFoundException(f"User with id '{id}' not found")

        return result

    def update(self, id: int, data: UserUpdate) -> User:
        """
        Update user.
        :param id: user id
        :param data: user update data
        :return: updated user model
        """
        user = self.get_one(id)
        if data.email is not None:
            user.email = data.email
        if data.username is not None:
            user.username = data.username
        self._db.session.add(user)
        self._db.session.commit()
        return user

    def create(self, user: UserCreate) -> User:
        """
        Create user.
        :param user: user model
        :return: created user model
        """
        user_dict = user.model_dump()

        # check if user with provided data already exists
        for field, value in user_dict.items():
            found_user_by_field = self._get_user_by_field(field, value)
            if found_user_by_field is not None:
                raise UserNotFoundException(
                    f"User with {field} '{value}' already exists"
                )

        user_model = User(**user.model_dump())
        self._db.session.add(user_model)
        self._db.session.flush()
        self._db.session.refresh(user_model)
        self._db.session.commit()
        return user_model

    def delete(self, id: int) -> None:
        """
        Delete user by id.
        :param id: user id
        """
        user = self.get_one(id)
        self._db.session.delete(user)
        self._db.session.commit()
        return None

    def get_all_filter_by_registered_date(
        self,
        days: int,
    ) -> list[User]:
        """
        Get all users filtered by registraion date
        :param days: number of days, positive number
        :return: list of users
        """
        timestamp_filter = (dt.now() - td(days=days)).isoformat()
        stmt = select(User).filter(User.registration_date > timestamp_filter)
        result = list(self._db.session.scalars(stmt).all())
        return result

    def get_order_by_longest_username(self, limit: int) -> list[User]:
        """
        Get top users with the longest username
        :param limit: positive number
        :return: list of users in top
        """
        if limit <= 0:
            raise ValueError("Limit must be positive number")

        stmt = (
            select(User)
            .order_by(func.char_length(User.username).desc())
            .limit(limit)
        )
        result = list(self._db.session.scalars(stmt).all())
        return result

    def get_count_matching_email_domain(self, domain: str) -> int:
        """
        Get count if all users with matched email domain
        :param domain: email domain
        :return: count of users
        """
        stmt = select(func.count(User.id)).filter(
            User.email.ilike(f"%{domain}")
        )
        result = self._db.session.scalar(stmt)

        return result or 0

    def get_all_count(self) -> int:
        """
        Get all users count
        :return: count of users
        """
        stmt = select(func.count(User.id))
        result = self._db.session.scalar(stmt)

        return result or 0
