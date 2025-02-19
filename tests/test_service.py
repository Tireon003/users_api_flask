import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

from app.src.models import User
from app.src.schemas.entities import UserFromDB
from app.src.services import UserService
from tests.conftest import client, users_data


@pytest.mark.usefixtures("client", "mock_db", "user_service")
class TestUserService:
    """Class for testing users service."""

    @pytest.fixture(autouse=True, scope='function')
    def _setup(self, mock_db: SQLAlchemy) -> None:
        """Setup fixture."""
        users = [User(**user) for user in users_data]
        mock_db.session.add_all(users)
        mock_db.session.commit()
        yield
        stmt = delete(User)
        mock_db.session.execute(stmt)
        mock_db.session.commit()

    def test_count_registered_last_week(
        self,
        user_service: UserService,
    ) -> None:
        """Test method counting number of users registered last week."""
        assert user_service.count_registered_last_week() == len(users_data)

    def test_get_top_5_longest_username(
        self,
        user_service: UserService,
    ) -> None:
        """Test method getting top 5 longest usernames."""
        top_from_service = user_service.get_top_5_longest_username()
        users_list_in_dict = [
            UserFromDB.model_validate(usr).model_dump()
            for usr in top_from_service
        ]
        assert len(top_from_service) <= 5
        for i in range(4):
            assert len(users_list_in_dict[i]["username"]) >= len(
                users_list_in_dict[i + 1]["username"]
            )

    @pytest.mark.parametrize(
        ("domain", "is_valid"),
        (
            ("gmail.com", True),
            ("gov.ru", True),
            ("google.com", True),
            ("mail", False),
            ("mail.r", False),
        ),
    )
    def test_get_proportion_with_domain(
        self,
        user_service: UserService,
        domain: str,
        is_valid: bool,
    ) -> None:
        """Test method getting proportion of provided domain."""

        if not is_valid:
            with pytest.raises(ValueError):
                user_service.get_proportion_with_domain(domain)
            return

        calculated_proportion = user_service.get_proportion_with_domain(domain)

        # calculating expected proportion
        email_generator = (item["email"] for item in users_data)
        domain_mapping = [email.endswith(domain) for email in email_generator]
        expected_proportion = round(
            domain_mapping.count(True) / len(domain_mapping), 2
        )

        assert calculated_proportion == expected_proportion
