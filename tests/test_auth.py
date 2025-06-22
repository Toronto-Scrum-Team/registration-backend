import os
import sys
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

sys.path.insert(0, os.getcwd())
from app.main import app

client = TestClient(app)


@pytest.fixture
def user_input_data():
    return {
        "email": "test3@example.com",
        "firstName": "Test",
        "lastName": "User",
        "password": "StrongPass!2",
        "confirmPassword": "StrongPass!2",
    }


def test_register_user_success(
    monkeypatch: pytest.MonkeyPatch, user_input_data: dict[str, str]
):
    # Mock DB
    mock_db = MagicMock()
    monkeypatch.setattr("app.routes.auth.get_db", lambda: print("mock_db"))

    # Pretend user does not already exist
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Mock password hash
    monkeypatch.setattr(
        "app.routes.auth.get_password_hash", lambda x: "hashedpassword123"
    )

    # Intercept adding and refreshing user
    def mock_add(user):
        user.id = "mocked-id"

    mock_db.add.side_effect = mock_add
    mock_db.refresh.side_effect = lambda user: user

    response = client.post("/auth/register", json=user_input_data)
    print(response.status_code, response.json())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == user_input_data["email"]
    assert "id" in response.json()


def test_login_user_success(monkeypatch: pytest.MonkeyPatch):
    credentials = {"email": "test3@example.com", "password": "StrongPass!2"}

    # Mock DB
    mock_db = MagicMock()
    monkeypatch.setattr("app.routes.auth.get_db", lambda: mock_db)

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


if __name__ == "__main__":
    pytest.main(["-s"])
