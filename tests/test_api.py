from typing import Any
import pytest
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

from app.src.models import User
from tests.conftest import client, users_data


@pytest.mark.usefixtures("client", "mock_db")
class TestUserAPI:
    """Class for testing API users."""

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

    @pytest.mark.parametrize(
        (
            "limit",
            "offset",
            "unexpected_param",
            "expected_response_json",
            "expected_response_status",
        ),
        [
            (0, 0, None, users_data, 200),
            (0, 1, None, users_data[1:], 200),
            (0, len(users_data), None, [], 200),
            (3, 2, None, users_data[2:5], 200),
            (
                0,
                0,
                1,
                {
                    "validation_error": {
                        "query_params": [
                            {
                                "input": "1",
                                "loc": ["unexpected_param"],
                                "msg": "Extra inputs are not permitted",
                                "type": "extra_forbidden",
                                "url": "https://errors.pydantic.dev/2.10/v/extra_forbidden",
                            }
                        ]
                    }
                },
                400,
            ),
        ],
    )
    def test_get_all_users(
        self,
        client: FlaskClient,
        limit: int,
        offset: int,
        unexpected_param: int | str | None,
        expected_response_status: int,
        expected_response_json: dict[str, Any],
    ) -> None:
        """Test for endpoint "get_all_users"."""
        url = f"/api/users/?limit={limit}&offset={offset}"
        if unexpected_param is not None:
            url += f"&unexpected_param={unexpected_param}"
        response = client.get(url)
        assert response.status_code == expected_response_status
        assert len(response.json) == len(expected_response_json)

    @pytest.mark.parametrize(
        ("user_id", "expected_user_data", "expected_response_status"),
        [
            (1, users_data[0], 200),
            (9, users_data[8], 200),
            (100, {"error": "User with id 100 not found"}, 404),
        ],
    )
    def test_get_user(
        self,
        client: FlaskClient,
        user_id: str,
        expected_response_status: int,
        expected_user_data: dict[str, Any],
    ) -> None:
        """Test for endpoint "get_user"."""
        url = f"/api/users/{user_id}/"
        response = client.get(url)
        assert response.status_code == expected_response_status
        if expected_response_status == 200:
            assert response.json["id"] == user_id
            assert response.json["username"] == expected_user_data["username"]
            assert response.json["email"] == expected_user_data["email"]
        if expected_response_status == 404:
            assert response.json == expected_user_data

    @pytest.mark.parametrize(
        (
            "request_body",
            "expected_response_status",
            "expected_response_json_key_values",
        ),
        [
            (
                {"username": "testuser1", "email": "testuser1@gmail.com"},
                201,
                {"username": "testuser1", "email": "testuser1@gmail.com"},
            ),
            (
                {"username": "johndoe", "email": "johndoe@google.com"},
                409,
                {"error": f"User with username 'johndoe' already exists"},
            ),
            (
                {"username": "johndoe123", "email": "johndoe@google.com"},
                409,
                {
                    "error": f"User with email 'johndoe@google.com' already exists"
                },
            ),
            (
                {"username": "testuser1", "email": f"{55*"a"}@gmail.com"},
                400,
                {
                    "validation_error": {
                        "body_params": [
                            {
                                "ctx": {
                                    "actual_length": 65,
                                    "field_type": "Value",
                                    "max_length": 64,
                                },
                                "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com",
                                "loc": ["email"],
                                "msg": "Value should have at most 64 items after validation, not 65",
                                "type": "too_long",
                                "url": "https://errors.pydantic.dev/2.10/v/too_long",
                            }
                        ]
                    }
                },
            ),
            (
                {"username": "tes", "email": "testuser1@gmail"},
                400,
                {
                    "validation_error": {
                        "body_params": [
                            {
                                "ctx": {
                                    "reason": "The part after the @-sign is not valid. It should have a period."
                                },
                                "input": "testuser1@gmail",
                                "loc": ["email"],
                                "msg": "value is not a valid email address: The part after the @-sign is not valid. It should have a period.",
                                "type": "value_error",
                            }
                        ]
                    }
                },
            ),
            (
                {"username": 33 * "a", "email": "a@b.c"},
                400,
                {
                    "validation_error": {
                        "body_params": [
                            {
                                "ctx": {"max_length": 32},
                                "input": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                "loc": ["username"],
                                "msg": "String should have at most 32 characters",
                                "type": "string_too_long",
                                "url": "https://errors.pydantic.dev/2.10/v/string_too_long",
                            },
                            {
                                "ctx": {
                                    "actual_length": 5,
                                    "field_type": "Value",
                                    "min_length": 6,
                                },
                                "input": "a@b.c",
                                "loc": ["email"],
                                "msg": "Value should have at least 6 items after validation, not 5",
                                "type": "too_short",
                                "url": "https://errors.pydantic.dev/2.10/v/too_short",
                            },
                        ]
                    }
                },
            ),
        ],
    )
    def test_create_user(
        self,
        client: FlaskClient,
        request_body: dict[str, Any],
        expected_response_status: int,
        expected_response_json_key_values: dict[str, Any],
    ) -> None:
        """Test for endpoint "create_user"."""
        url = "/api/users/"
        response = client.post(url, json=request_body)
        assert response.status_code == expected_response_status
        for key, val in expected_response_json_key_values.items():
            assert val == response.json.get(key)

    @pytest.mark.parametrize(
        ("user_id", "request_body", "expected_response_status"),
        (
            (
                1,
                {"username": "johndoe1", "email": "johndoe1@google.com"},
                200,
            ),
            (
                1,
                {"username": "johndoe", "email": "johndoe12@google.com"},
                200,
            ),
            (
                1,
                {"username": "johndoe123", "email": "johndoe@google.com"},
                200,
            ),
            (
                10,
                {"username": "supersuperuser", "email": "notuser@google.com"},
                404,
            ),
            (
                2,
                {"username": "spongebob", "email": "tony_stark@mtuci.ru"},
                409,
            ),
            (
                7,
                {
                    "username": "petrov_igor",
                    "email": "daniel_defau@rambler.com",
                },
                409,
            ),
        ),
    )
    def test_update_user(
        self,
        client: FlaskClient,
        user_id: int,
        request_body: dict[str, Any],
        expected_response_status: int,
    ) -> None:
        """Test for endpoint "update_user"."""
        url = f"/api/users/{user_id}/"
        response = client.patch(url, json=request_body)
        assert response.status_code == expected_response_status

    @pytest.mark.parametrize(
        ("user_id", "expected_response_status", "expected_response_json"),
        (
            (1, 200, {"message": f"User with id 1 deleted"}),
            (112, 404, {"error": f"User with id 112 not found"}),
        ),
    )
    def test_delete_user(
        self,
        client: FlaskClient,
        user_id: int,
        expected_response_status: int,
        expected_response_json: dict[str, Any],
    ) -> None:
        """Test for endpoint "delete_user"."""
        url = f"/api/users/{user_id}/"
        response = client.delete(url)
        assert response.status_code == expected_response_status
        assert response.json == expected_response_json

    def test_get_users_registered_from_last_week(
        self,
        client: FlaskClient,
    ) -> None:
        """Test for endpoint "get_users_registered_from_last_week"."""
        url = "/api/users/stats/from_last_week"
        response = client.get(url)
        assert response.status_code == 200
        assert response.json == {"count": len(users_data)}

    @pytest.mark.parametrize(
        (
            "domain",
            "expected_response_status",
        ),
        (
            ("gmail.com", 200),
            ("gov.ru", 200),
            ("google.com", 200),
            ("mail", 400),
        ),
    )
    def test_get_users_with_email_domain(
        self,
        client: FlaskClient,
        domain: str,
        expected_response_status: int,
    ) -> None:
        """Test for endpoint "get_users_with_email_domain"."""
        url = f"/api/users/stats/with_email_domain/{domain}"
        email_generator = (item["email"] for item in users_data)
        domain_mapping = [email.endswith(domain) for email in email_generator]
        expected_proportion = round(
            domain_mapping.count(True) / len(domain_mapping), 2
        )
        response = client.get(url)
        assert response.status_code == expected_response_status
        if expected_response_status == 200:
            assert response.json["domain"] == domain
            assert response.json["proportion"] == expected_proportion

    def test_get_top_5_longest_username(
        self,
        client: FlaskClient,
    ) -> None:
        """Test for endpoint "get_top_5_longest_username"."""
        url = "/api/users/stats/top_longest_username"
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.json) <= 5
        for i in range(4):
            assert len(response.json[i]["username"]) >= len(
                response.json[i + 1]["username"]
            )
