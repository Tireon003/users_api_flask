from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from pydantic_settings import SettingsConfigDict

from app.main import create_app
from app.config import Settings
from app.src.core import db
from app.src.repositories import UserRepository
from app.src.services import UserService

users_data = [
    {"username": "johndoe", "email": "johndoe@google.com"},
    {"username": "spongebob", "email": "spongebob@google.com"},
    {"username": "petrov_igor", "email": "igorpetrov@yandex.ru"},
    {"username": "sergey_ivanov", "email": "sergey_ivanov@mail.ru"},
    {"username": "bruce_wayne", "email": "bruce_wayne@gmail.com"},
    {"username": "tony_stark", "email": "tony_stark@mtuci.ru"},
    {"username": "daniel_defau", "email": "daniel_defau@rambler.com"},
    {"username": "dilon_d", "email": "dilon_d@inbox.ru"},
    {"username": "marina_sm1", "email": "marinasmirnova@mtuci.ru"},
]


class MockSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env_test")


@pytest.fixture(scope="session")
def app_settings() -> MockSettings:
    """Фикстура для настроек приложения"""
    return MockSettings()


@pytest.fixture(scope="session")
def app(app_settings: MockSettings) -> Generator[Flask, None, None]:
    """Фикстура Flask приложения с базой данных"""
    _app = create_app(app_settings)
    _app.config.update({"TESTING": True})

    with _app.app_context():
        db.create_all()

        yield _app

        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Фикстура для тестового клиента Flask"""
    return app.test_client()


@pytest.fixture
def mock_db() -> SQLAlchemy:
    """Фикстура для доступа к базе данных"""
    return db


@pytest.fixture
def user_service(mock_db: SQLAlchemy) -> UserService:
    repo = UserRepository(mock_db)
    return UserService(repo)
