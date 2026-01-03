def test_create_user_success(client):
    client_app, mocks = client
    payload = {"username": "john"}

    mocks["user"].create_user.return_value = {"id": 1, "username": "john"}

    response = client_app.post("/users/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "john"}
    mocks["user"].create_user.assert_called_once()


def test_create_user_already_exists(client):
    client_app, mocks = client
    payload = {"username": "john"}

    mocks["user"].create_user.side_effect = ValueError("User already exists")

    response = client_app.post("/users/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    mocks["user"].create_user.assert_called_once()


def test_get_user_found(client):
    client_app, mocks = client
    mocks["user"].get_user.return_value = {"id": 1, "username": "alice"}

    response = client_app.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "alice"}
    mocks["user"].get_user.assert_called_once_with(1)


def test_get_user_not_found(client):
    client_app, mocks = client
    mocks["user"].get_user.return_value = None

    response = client_app.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    mocks["user"].get_user.assert_called_once_with(999)


