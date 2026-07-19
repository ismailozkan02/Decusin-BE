import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_login_wrong_credentials():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_me_unauthenticated():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
