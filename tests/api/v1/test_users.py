import random
import string
from typing import Dict
import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


@pytest.fixture
def new_user_data() -> Dict[str, str]:
    return {"email": random_email(), "full_name": "Test User", "password": random_lower_string()}


USERS_ENDPOINT = f"{settings.API_VER_STR}/users"


def test_create_user(test_client: TestClient, new_user_data: Dict[str, str]) -> None:
    response = test_client.post(USERS_ENDPOINT, json=new_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_user_data["email"]


def test_create_existing_user(test_client: TestClient, new_user_data: Dict[str, str]) -> None:
    fixed_user_info = new_user_data.copy()
    response = test_client.post(USERS_ENDPOINT, json=fixed_user_info)
    assert response.status_code == 200

    response = test_client.post(USERS_ENDPOINT, json=fixed_user_info)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_read_user(test_client: TestClient, new_user_data: Dict[str, str]) -> None:
    fixed_user_info = new_user_data.copy()
    response = test_client.post(USERS_ENDPOINT, json=fixed_user_info)
    assert response.status_code == 200
    created_user = response.json()

    response = test_client.get(f"{USERS_ENDPOINT}/{created_user['id']}")
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == fixed_user_info["email"]


def test_update_user(test_client: TestClient, new_user_data: Dict[str, str]) -> None:
    # Create the user
    response = test_client.post(USERS_ENDPOINT, json=new_user_data)
    assert response.status_code == 200
    created_user = response.json()

    # Update the user
    updated_data = {
        "id": created_user["id"],
        "email": created_user["email"],
        "full_name": "Updated User",
        "hashed_password": created_user["hashed_password"],
    }
    response = test_client.put(f"{USERS_ENDPOINT}/{created_user['id']}", json=updated_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["full_name"] == "Updated User"


def test_delete_user(test_client: TestClient, new_user_data: Dict[str, str]) -> None:
    # Create the user
    response = test_client.post(USERS_ENDPOINT, json=new_user_data)
    assert response.status_code == 200
    created_user = response.json()
    # Delete the user
    response = test_client.delete(f"{USERS_ENDPOINT}/{created_user['id']}")
    assert response.status_code == 200
    assert response.json() is True

    # Try to read the deleted user
    response = test_client.get(f"{USERS_ENDPOINT}/{created_user['id']}")
    assert response.status_code == 404
