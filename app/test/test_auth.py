from fastapi import status
from fastapi.testclient import TestClient


def test_login_correct(client: TestClient):
    response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    login_response = client.post(
        "/login", data={"username": "example@example.com", "password": "example"}
    )
    assert login_response.status_code == status.HTTP_200_OK


def test_login_user_not_found(client: TestClient):
    response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    login_response = client.post(
        "/login", data={"username": "email@invalid.com", "password": "example"}
    )
    assert login_response.status_code == status.HTTP_404_NOT_FOUND


def test_login_bad_request(client: TestClient):
    response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    login_response = client.post(
        "/login", data={"username": "example@example.com", "password": "ex"}
    )
    assert login_response.status_code == status.HTTP_400_BAD_REQUEST
