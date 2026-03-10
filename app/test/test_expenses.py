from fastapi import status
from fastapi.testclient import TestClient

from app.models.expense_model import CategoryEnum


def test_list_expenses(client: TestClient):
    list_response = client.get("/expenses")
    assert list_response.status_code == status.HTTP_200_OK


def test_add_expense(client: TestClient):
    expense_data = {
        "description": "Description example",
        "ammount": 20.25,
        "category": "groceries",
    }
    add_response = client.post("/expenses", json=expense_data)
    assert add_response.status_code == status.HTTP_201_CREATED


def test_add_expense_bad_request(client: TestClient):
    expense_data = {
        "description": "Example bad request for Expense",
    }
    add_response = client.post("/expenses", json=expense_data)
    assert add_response.status_code == status.HTTP_400_BAD_REQUEST


def test_read_expense(client: TestClient):
    expense_data = {
        "description": "Description example",
        "ammount": 20.25,
        "category": "groceries",
    }
    add_response = client.post("/expenses", json=expense_data)
    assert add_response.status_code == status.HTTP_201_CREATED
    expense_id = add_response.json()["id"]
    read_response = client.get(f"/expenses/{expense_id}")
    assert read_response.status_code == status.HTTP_200_OK


def test_read_expense_not_found(client: TestClient):
    expense_id = 999
    read_response = client.get(f"/expenses/{expense_id}")
    assert read_response.status_code == status.HTTP_404_NOT_FOUND


# def test_read_expense_unauthorized(client: TestClient):
#     expense_data = {
#         "description": "Description example",
#         "ammount": 20.25,
#         "category": "groceries",
#     }
#     add_response = client.post("/expenses", json=expense_data)
#     assert add_response.status_code == status.HTTP_201_CREATED
#     expense_id = add_response.json()["id"]
#     read_response = client.get(f"/expenses/{expense_id}")
#     assert read_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_expense(client: TestClient):
    expense_data = {
        "description": "Description example",
        "ammount": 20.25,
        "category": "groceries",
    }
    add_response = client.post("/expenses", json=expense_data)
    assert add_response.status_code == status.HTTP_201_CREATED
    expense_id: int = add_response.json()["id"]
    update_data = {"ammount": 50.50, "category": CategoryEnum.ELECTRONICS}
    update_response = client.patch(f"/expenses/{expense_id}", json=update_data)
    print(update_response.json())
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["ammount"] == update_data["ammount"]


def test_update_expense_not_found(client: TestClient):
    expense_id: int = 999
    update_data = {"ammount": 50.50, "category": CategoryEnum.ELECTRONICS}
    update_response = client.patch(f"/expenses/{expense_id}", json=update_data)
    print(update_response.json())
    assert update_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_expense(client: TestClient):
    expense_data = {
        "description": "Description example",
        "ammount": 20.25,
        "category": "groceries",
    }
    add_response = client.post("/expenses", json=expense_data)
    assert add_response.status_code == status.HTTP_201_CREATED
    expense_id: int = add_response.json()["id"]
    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_not_found(client: TestClient):
    expense_id = 999
    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
