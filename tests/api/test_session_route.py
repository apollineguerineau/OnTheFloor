def test_create_session(client):
    client_app, mocks = client

    payload = {
        "name": "Morning WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": 1
    }

    mocks["session"].create_session.return_value = {
        "id": 0,
        "name": "Morning WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": 1
    }

    response = client_app.post("/sessions/", json=payload)
    assert response.status_code == 200
    print(f"response api : {response.json()}")
    assert response.json() == mocks["session"].create_session.return_value


def test_create_session_invalid_location(client):
    client_app, mocks = client
    mocks["session"].create_session.side_effect = ValueError("Location with id 99 not found")

    payload = {
        "name": "WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id": 1,
        "location_id": 99
    }

    response = client_app.post("/sessions/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Location with id 99 not found"


def test_get_session_found(client):
    client_app, mocks = client
    mock_session = {
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": None
    }
    mocks["session"].get_session.return_value = mock_session

    response = client_app.get("/sessions/1")
    assert response.status_code == 200
    assert response.json() == mock_session


def test_get_session_not_found(client):
    client_app, mocks = client
    mocks["session"].get_session.return_value = None

    response = client_app.get("/sessions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_get_session_by_date_found(client):
    client_app, mocks = client
    mock_session = [{
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": 1
    }]
    mocks["session"].get_sessions_by_date.return_value = mock_session

    response = client_app.get("/sessions/by-date/?session_date=2026-01-01&user_id=1")
    assert response.status_code == 200
    assert response.json() == mock_session

def test_list_sessions_by_user(client):
    client_app, mocks = client
    mock_list = [{
        "id": 1,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": None
    }]
    mocks["session"].list_sessions_by_user.return_value = mock_list

    response = client_app.get("/sessions/user/1")
    assert response.status_code == 200
    assert response.json() == mock_list

def test_get_sessions_by_location(client):
    client_app, mocks = client
    mocks["session"].get_sessions_by_location.return_value = [
        {
            "id": 1,
            "name": "Morning WOD",
            "date": "2026-01-01",
            "session_type": "WOD",
            "user_id": 2,
            "notes": "Fun!",
            "location_id": 1
        }
    ]
    response = client_app.get("/sessions/by-location/?location_id=1&user_id=2")
    assert response.status_code == 200
    assert response.json() == mocks["session"].get_sessions_by_location.return_value


def test_update_session_success(client):
    client_app, mocks = client
    payload = {"name": "Updated WOD", "location_id": 2}
    mock_updated = {
        "id": 1,
        "name": "Updated WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id": 1,
        "notes": "Fun!",
        "location_id": 2
    }
    mocks["session"].update_session.return_value = mock_updated

    response = client_app.patch("/sessions/1", json=payload)
    assert response.status_code == 200
    assert response.json() == mock_updated


def test_update_session_not_found(client):
    client_app, mocks = client
    mocks["session"].update_session.side_effect = ValueError("Session not found")

    response = client_app.patch("/sessions/999", json={"name": "WOD"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

def test_delete_session_success(client):
    client_app, mocks = client

    response = client_app.delete("/sessions/1")
    assert response.status_code == 204
    mocks["session"].delete_session.assert_called_once_with(1)


def test_delete_session_not_found(client):
    client_app, mocks = client
    mocks["session"].delete_session.side_effect = ValueError("Session not found")

    response = client_app.delete("/sessions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

