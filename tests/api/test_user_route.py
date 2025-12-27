from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.api.schemas.user import UserCreate
from src.data.models import User


def test_create_user_success(client):
    payload = {"username": "john"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "john"
    assert "id" in data

def test_create_user_duplicate(client):
    payload = {"username": "john"}
    client.post("/users/", json=payload)  # crée l'utilisateur
    response = client.post("/users/", json=payload)  # essai de créer le même
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

