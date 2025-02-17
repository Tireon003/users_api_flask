from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from app.src.exceptions import UserNotFoundException
from app.src.models import User
from app.src.schemas.entities import UserUpdate, UserCreate
from app.src.schemas.query import UserPaginatorQueryParams


class UserRepository:
    """
    Repository class for User model.
    """

    def __init__(self, db: SQLAlchemy) -> None:
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
        stmt = (
            select(User)
            .offset(paginator_params.offset)
            .limit(paginator_params.limit)
        )
        result = list(self._db.session.scalars(stmt).all())
        return result

    def _get_user_by_field(self, field_name: str, value: str) -> User | None:
        """
        Get user by field. Service method.
        :param field_name: field name
        :param value: field value
        :return: user
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
        :return: updated user
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
        :return: created user
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
