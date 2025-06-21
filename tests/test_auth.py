import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.getcwd())
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_user_data():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword123",
    }


def test_register_user_success(mock_user_data, mocker):
    # Mock the function that creates a new user
    mock_create_user = mocker.patch("app.routes.auth.create_user")
    mock_create_user.return_value = {
        "id": 1,
        "username": mock_user_data["username"],
        "email": mock_user_data["email"],
    }

    response = client.post("/register", json=mock_user_data)

    assert response.status_code == 201
    assert response.json()["username"] == mock_user_data["username"]


def test_login_user_success(mock_user_data, mocker):
    # Mock authentication
    mock_authenticate_user = mocker.patch("app.routes.auth.authenticate_user")
    mock_authenticate_user.return_value = {
        "id": 1,
        "username": mock_user_data["username"],
    }

    # Mock JWT token creation
    mock_create_token = mocker.patch("app.routes.auth.create_access_token")
    mock_create_token.return_value = "mocked.jwt.token"

    response = client.post(
        "/login",
        data={
            "username": mock_user_data["username"],
            "password": mock_user_data["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "mocked.jwt.token"
