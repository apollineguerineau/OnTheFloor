

def test_create_exercise(client):
    client_app, mocks = client

    payload = {
        "exercise_type": "Deadlift",
        "session_id": 1,
        "position": 0,
        "weight_kg": 50.0,
        "repetitions": 10,
        "notes": "Fast"
    }

    mocks["exercise"].create_exercise.return_value = {
        "id": 1,
        "exercise_type": "Deadlift",
        "session_id": 1,
        "position": 0,
        "block_id": None,
        "weight_kg": 50.0,
        "repetitions": 10,
        "duration_seconds": None,
        "distance_meters": None,
        "position_in_block": None,
        "notes": "Fast"
    }

    response = client_app.post("/exercises/", json=payload)

    assert response.status_code == 200
    assert response.json() == mocks["exercise"].create_exercise.return_value


def test_create_exercise_session_not_found(client):
    client_app, mocks = client
    mocks["exercise"].create_exercise.side_effect = ValueError("Session not found")

    payload = {
        "exercise_type": "Deadlift",
        "session_id": 99
    }

    response = client_app.post("/exercises/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Session not found"


def test_get_exercise_found(client):
    client_app, mocks = client

    mock_exercise = {
        "id": 1,
        "exercise_type": "Deadlift",
        "session_id": 1,
        "block_id": None,
        "position": 0,
        "position_in_block": None,
        "weight_kg": 50.0,
        "repetitions": 10,
        "duration_seconds": None,
        "distance_meters": None,
        "notes": "Fast"
    }

    mocks["exercise"].get_exercise.return_value = mock_exercise

    response = client_app.get("/exercises/1")

    assert response.status_code == 200
    assert response.json() == mock_exercise


def test_get_exercise_not_found(client):
    client_app, mocks = client
    mocks["exercise"].get_exercise.return_value = None

    response = client_app.get("/exercises/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"


def test_list_exercises_by_session(client):
    client_app, mocks = client

    mock_exercises = [
        {
            "id": 1,
            "exercise_type": "Deadlift",
            "session_id": 1,
            "block_id": None,
            "position": 0,
            "position_in_block": None,
            "weight_kg": 50.0,
            "repetitions": 10,
            "duration_seconds": None,
            "distance_meters": None,
            "notes": None
        },
        {
            "id": 2,
            "exercise_type": "Deadlift",
            "session_id": 1,
            "block_id": 1,
            "position": None,
            "position_in_block": 0,
            "weight_kg": None,
            "repetitions": 15,
            "duration_seconds": 12,
            "distance_meters": None,
            "notes": "Heavy"
        }
    ]

    mocks["exercise"].list_by_session.return_value = mock_exercises

    response = client_app.get("/exercises/session/1")

    assert response.status_code == 200
    assert response.json() == mock_exercises


def test_update_exercise_success(client):
    client_app, mocks = client

    payload = {
        "position": 2,
        "notes": "Updated notes"
    }

    mock_updated = {
        "id": 1,
        "exercise_type": "Deadlift",
        "session_id": 1,
        "block_id": None,
        "position": 2,
        "position_in_block": None,
        "weight_kg": 50.0,
        "repetitions": 10,
        "duration_seconds": None,
        "distance_meters": None,
        "notes": "Updated notes"
    }

    mocks["exercise"].update_exercise.return_value = mock_updated

    response = client_app.patch("/exercises/1", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_updated


def test_update_exercise_not_found(client):
    client_app, mocks = client
    mocks["exercise"].update_exercise.side_effect = ValueError("Exercise not found")

    response = client_app.patch("/exercises/999", json={"position": 1})

    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"


def test_delete_exercise_success(client):
    client_app, mocks = client

    response = client_app.delete("/exercises/1")

    assert response.status_code == 204
    mocks["exercise"].delete_exercise.assert_called_once_with(1)


def test_delete_exercise_not_found(client):
    client_app, mocks = client
    mocks["exercise"].delete_exercise.side_effect = ValueError("Exercise not found")

    response = client_app.delete("/exercises/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Exercise not found"
