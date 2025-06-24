import os
import sys
from datetime import datetime as dt
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

sys.path.insert(0, os.getcwd())
from app.database import get_db
from app.main import app
from app.routes.auth import validate_password_strength

client = TestClient(app)


@pytest.mark.parametrize(
    "password,expected",
    [
        # Too short
        ("A1!", False),
        ("abcD1!", False),
        # Missing uppercase
        ("password1!", False),
        # Missing number
        ("Password!", False),
        # Missing special character
        ("Password1", False),
        # Unexpected special character
        ("Password1~", False),
        # All criteria met
        ("Password1!", True),
        ("A1b2C3d4!", True),
        ("My$ecureP@ssw0rd", True),
    ],
)
def test_validate_password_strength(password, expected):
    assert validate_password_strength(password) == expected


@pytest.fixture
def user_input_data():
    return {
        "email": "test7@example.com",
        "firstName": "Test",
        "lastName": "User",
        "password": "StrongPass!2",
        "confirmPassword": "StrongPass!2",
    }


def test_register_passwords_do_not_match(user_input_data):
    user_data = user_input_data.copy()
    user_data["confirmPassword"] = "Mismatch123!"

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "passwords" in response.text.lower()


def test_register_short_weak_password(user_input_data):
    """Handled by Pydantic (schema definition)"""
    user_data = user_input_data.copy()
    user_data["password"] = "weak"
    user_data["confirmPassword"] = "weak"

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "password" in response.text.lower()


def test_register_long_weak_password(user_input_data):
    user_data = user_input_data.copy()
    user_data["password"] = "weakpass"
    user_data["confirmPassword"] = "weakpass"

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.text.lower()


def test_register_missing_fields():
    user_data = {
        "email": "",
        "firstName": "",
        "lastName": "",
        "password": "",
        "confirmPassword": "",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_existing_email(user_input_data):
    # Mock DB returning a user (email already exists)
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    response = client.post("/auth/register", json=user_input_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.text.lower()

    # Clean up override
    app.dependency_overrides = {}


def test_register_user_success(
    monkeypatch: pytest.MonkeyPatch, user_input_data: dict[str, str]
):
    # Mock DB
    mock_db = MagicMock()

    # Simulate "user not found" when checking for existing email
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Override get_db dependency
    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    # Mock password hash
    monkeypatch.setattr(
        "app.routes.auth.get_password_hash", lambda x: "hashedpassword123"
    )

    # Intercept adding and refreshing user
    def mock_add(user):
        user.id = "mocked-id"
        user.created_at = dt.now()

    mock_db.add.side_effect = mock_add
    mock_db.refresh.side_effect = lambda user: user

    response = client.post("/auth/register", json=user_input_data)
    print(response.status_code, response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_input_data["email"]
    assert "id" in response.json()
    # Clean up override
    app.dependency_overrides = {}


def test_login_user_success(monkeypatch: pytest.MonkeyPatch):
    credentials = {"email": "test7@example.com", "password": "StrongPass!2"}

    # Mock DB
    mock_db = MagicMock()

    # Override get_db dependency
    def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    # Fake user returned from DB
    fake_user = MagicMock()
    fake_user.email = credentials["email"]
    fake_user.hashed_password = "hashedpass"
    mock_db.query.return_value.filter.return_value.first.return_value = fake_user

    # Mock password check and session/token generation
    monkeypatch.setattr("app.routes.auth.verify_password", lambda p, h: True)
    monkeypatch.setattr(
        "app.routes.auth.create_session",
        lambda db, u, info: MagicMock(session_id="abc-123"),
    )
    monkeypatch.setattr(
        "app.routes.auth.create_access_token_with_session",
        lambda data, session_id: "fake.jwt.token",
    )

    response = client.post("/auth/login", json=credentials)

    assert response.status_code == 200
    assert response.json()["access_token"] == "fake.jwt.token"

    # Clean up override
    app.dependency_overrides = {}


if __name__ == "__main__":
    pytest.main(["-s"])
