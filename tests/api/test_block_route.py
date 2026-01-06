def test_create_block(client):
    client_app, mocks = client

    payload = {
        "block_type": "AMRAP",
        "position": 1,
        "session_id": 1,
        "duration": 15.0,
        "notes": "Warm-up"
    }

    mocks["block"].create_block.return_value = {
        "id": 1,
        "block_type": "AMRAP",
        "position": 1,
        "session_id": 1,
        "duration": 15.0,
        "notes": "Warm-up"
    }

    response = client_app.post("/blocks/", json=payload)

    assert response.status_code == 200
    assert response.json() == mocks["block"].create_block.return_value


def test_create_block_session_not_found(client):
    client_app, mocks = client
    mocks["block"].create_block.side_effect = ValueError("Session not found")

    payload = {
        "block_type": "EMOM",
        "position": 1,
        "session_id": 99
    }

    response = client_app.post("/blocks/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"


def test_get_block_found(client):
    client_app, mocks = client
    mock_block = {
        "id": 1,
        "block_type": "AMRAP",
        "position": 1,
        "session_id": 1,
        "duration": 12.0,
        "notes": None
    }
    mocks["block"].get_block.return_value = mock_block

    response = client_app.get("/blocks/1")

    assert response.status_code == 200
    assert response.json() == mock_block


def test_get_block_not_found(client):
    client_app, mocks = client
    mocks["block"].get_block.return_value = None

    response = client_app.get("/blocks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Block not found"


def test_list_blocks_by_session(client):
    client_app, mocks = client
    mock_blocks = [
        {
            "id": 1,
            "block_type": "AMRAP",
            "position": 1,
            "session_id": 1,
            "duration": 10.0,
            "notes": None
        },
        {
            "id": 2,
            "block_type": "EMOM",
            "position": 2,
            "session_id": 1,
            "duration": 12.0,
            "notes": "Heavy"
        }
    ]
    mocks["block"].list_blocks_by_session.return_value = mock_blocks

    response = client_app.get("/blocks/session/1")

    assert response.status_code == 200
    assert response.json() == mock_blocks


def test_update_block_success(client):
    client_app, mocks = client

    payload = {
        "position": 2,
        "notes": "Updated notes"
    }

    mock_updated = {
        "id": 1,
        "block_type": "AMRAP",
        "position": 2,
        "session_id": 1,
        "duration": 15.0,
        "notes": "Updated notes"
    }

    mocks["block"].update_block.return_value = mock_updated

    response = client_app.patch("/blocks/1", json=payload)

    assert response.status_code == 200
    assert response.json() == mock_updated


def test_update_block_not_found(client):
    client_app, mocks = client
    mocks["block"].update_block.side_effect = ValueError("Block not found")

    response = client_app.patch("/blocks/999", json={"position": 1})

    assert response.status_code == 404
    assert response.json()["detail"] == "Block not found"


def test_delete_block_success(client):
    client_app, mocks = client

    response = client_app.delete("/blocks/1")

    assert response.status_code == 204
    mocks["block"].delete_block.assert_called_once_with(1)


def test_delete_block_not_found(client):
    client_app, mocks = client
    mocks["block"].delete_block.side_effect = ValueError("Block not found")

    response = client_app.delete("/blocks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Block not found"
