from uuid import UUID

def test_create_session(client, user_id, location_id, session_id):
    client_app, mocks = client

    payload = {
        "name": "Morning WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id":location_id
    }

    mocks["session"].create_session.return_value = {
        "id":session_id,
        "name": "Morning WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id":location_id
    }

    response = client_app.post("/sessions/", json=payload)
    assert response.status_code == 200
    print(f"response api : {response.json()}")
    assert response.json() == mocks["session"].create_session.return_value


def test_create_session_invalid_location(client, user_id, location_id):
    client_app, mocks = client
    mocks["session"].create_session.side_effect = ValueError("Location with id 99 not found")

    payload = {
        "name": "WOD",
        "date": "2026-01-01",
        "session_type": "WOD",
        "user_id":user_id,
        "location_id":location_id
    }

    response = client_app.post("/sessions/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Location with id 99 not found"


def test_get_session_found(client, user_id, session_id):
    client_app, mocks = client
    mock_session = {
        "id":session_id,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id": None
    }
    mocks["session"].get_session.return_value = mock_session

    response = client_app.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json() == mock_session


def test_get_session_not_found(client, session_id):
    client_app, mocks = client
    mocks["session"].get_session.return_value = None

    response = client_app.get(f"/sessions/{session_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_get_session_by_date_found(client, user_id, location_id, session_id):
    client_app, mocks = client
    mock_session = [{
        "id":session_id,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id":location_id
    }]
    mocks["session"].get_sessions_by_date.return_value = mock_session

    response = client_app.get(f"/sessions/by-date/?session_date=2026-01-01&user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == mock_session

def test_list_sessions_by_user(client, user_id, session_id):
    client_app, mocks = client
    mock_list = [{
        "id":session_id,
        "name": "Morning WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id": None
    }]
    mocks["session"].list_sessions_by_user.return_value = mock_list

    response = client_app.get(f"/sessions/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == mock_list

def test_get_sessions_by_location(client, user_id, location_id, session_id):
    client_app, mocks = client
    mocks["session"].get_sessions_by_location.return_value = [
        {
            "id":session_id,
            "name": "Morning WOD",
            "date": "2026-01-01",
            "session_type": "WOD",
            "user_id":user_id,
            "notes": "Fun!",
            "location_id":location_id
        }
    ]
    response = client_app.get(f"/sessions/by-location/?location_id={location_id}&user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == mocks["session"].get_sessions_by_location.return_value


def test_update_session_success(client, user_id, location_id, session_id):
    client_app, mocks = client
    payload = {"name": "Updated WOD", "location_id":location_id}
    mock_updated = {
        "id":session_id,
        "name": "Updated WOD",
        "date": '2026-01-01',
        "session_type": "WOD",
        "user_id":user_id,
        "notes": "Fun!",
        "location_id":location_id
    }
    mocks["session"].update_session.return_value = mock_updated

    response = client_app.patch(f"/sessions/{session_id}", json=payload)
    assert response.status_code == 200
    assert response.json() == mock_updated


def test_update_session_not_found(client, session_id):
    client_app, mocks = client
    mocks["session"].update_session.side_effect = ValueError("Session not found")

    response = client_app.patch(f"/sessions/{session_id}", json={"name": "WOD"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

def test_delete_session_success(client, session_id):
    client_app, mocks = client

    response = client_app.delete(f"/sessions/{session_id}")
    assert response.status_code == 204
    mocks["session"].delete_session.assert_called_once_with(UUID(session_id))


def test_delete_session_not_found(client, session_id):
    client_app, mocks = client
    mocks["session"].delete_session.side_effect = ValueError("Session not found")

    response = client_app.delete(f"/sessions/{session_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

