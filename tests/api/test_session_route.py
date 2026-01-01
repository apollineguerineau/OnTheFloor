import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from src.main import app

@pytest.fixture
def client(monkeypatch):
    """Fixture qui mocke SessionService pour toutes les routes."""
    mock_service_instance = MagicMock()
    # On remplace la classe SessionService par un lambda qui retourne le mock
    monkeypatch.setattr(
        "src.api.routes.session.SessionService",
        lambda db=None: mock_service_instance
    )
    return TestClient(app), mock_service_instance


def test_create_session(client):
    client_app, mock_service = client
    payload = {"name": "Morning WOD", "date": "2026-01-01", "session_type": "WOD", "user_id": 1, "notes": "Fun!"}

    mock_service.create_session.return_value = {"id": 0,"name": "Morning WOD", "date": "2026-01-01", "session_type": "WOD", "user_id": 1, "notes": "Fun!"}

    response = client_app.post("/sessions/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": 0,"name": "Morning WOD", "date": "2026-01-01", "session_type": "WOD", "user_id": 1, "notes": "Fun!"}


def test_get_session_found(client):
    client_app, mock_service = client
    mock_session = {
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!"
    }
    mock_service.get_session.return_value = mock_session

    response = client_app.get("/sessions/1")
    assert response.status_code == 200
    assert response.json() == mock_session


def test_get_session_not_found(client):
    client_app, mock_service = client
    mock_service.get_session.return_value = None

    response = client_app.get("/sessions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_get_session_by_date_found(client):
    client_app, mock_service = client
    mock_session = {
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!"
    }
    mock_service.get_session_by_date.return_value = mock_session

    response = client_app.get("/sessions/by-date/?session_date=2026-01-01&user_id=1")
    assert response.status_code == 200
    assert response.json() == mock_session

def test_get_session_by_date_not_found(client):
    client_app, mock_service = client
    mock_service.get_session_by_date.return_value = None

    response = client_app.get("/sessions/by-date/?session_date=2026-01-01&user_id=1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_list_sessions_by_user(client):
    client_app, mock_service = client
    mock_list = [{
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!"
    }]
    mock_service.list_sessions_by_user.return_value = mock_list

    response = client_app.get("/sessions/user/1")
    assert response.status_code == 200
    assert response.json() == mock_list


def test_update_session_success(client):
    client_app, mock_service = client
    payload = {"name": "Updated WOD"}
    mock_updated = {
        "id": 1,
        "name": "Updated WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!"
    }
    mock_service.update_session.return_value = mock_updated

    response = client_app.patch("/sessions/1", json=payload)
    assert response.status_code == 200
    assert response.json() == mock_updated

def test_update_session_not_found(client):
    client_app, mock_service = client
    mock_service.update_session.side_effect = ValueError("Session not found")

    response = client_app.patch("/sessions/999", json={"name": "WOD"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_delete_session_success(client):
    client_app, mock_service = client

    response = client_app.delete("/sessions/1")
    assert response.status_code == 204
    mock_service.delete_session.assert_called_once_with(1)


def test_delete_session_not_found(client):
    client_app, mock_service = client
    mock_service.delete_session.side_effect = ValueError("Session not found")

    response = client_app.delete("/sessions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"
