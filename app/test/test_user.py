from fastapi import status
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_invalid_content(client: TestClient):
    create_response = client.post(
        "/register",
        json={
            "email": "example$invalid.email",
            "password": "example",
            "name": "Example",
        },
    )
    assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_bad_request(client: TestClient):
    create_response = client.post(
        "/register",
        json={
            "password": "example",
            "name": "Example",
        },
    )
    assert create_response.status_code == status.HTTP_400_BAD_REQUEST


def test_upate_user(client: TestClient):
    create_response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id: int = create_response.json()["id"]
    email_update = "update@example.com"
    update_response = client.patch(
        f"/register/{user_id}",
        json={"email": email_update},
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["email"] == email_update


def test_update_user_not_found(client: TestClient):
    create_response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id: int = 999
    email_update = "update@example.com"
    update_response = client.patch(f"/register/{user_id}", json={"email": email_update})
    assert update_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(client: TestClient):
    create_response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id: int = create_response.json()["id"]
    delete_response = client.delete(f"/register/{user_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_not_found(client: TestClient):
    create_response = client.post(
        "/register",
        json={"email": "example@example.com", "password": "example", "name": "Example"},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id: int = 999
    delete_response = client.delete(f"/register/{user_id}")
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
