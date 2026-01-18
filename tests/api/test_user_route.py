from uuid import UUID

def test_create_user_success(client, user_id):
    client_app, mocks = client
    payload = {"username": "john"}

    mocks["user"].create_user.return_value = {"id":user_id, "username": "john"}

    response = client_app.post("/users/", json=payload)

    assert response.status_code == 200
    assert response.json() == {"id":user_id, "username": "john"}
    mocks["user"].create_user.assert_called_once()


def test_create_user_already_exists(client, user_id):
    client_app, mocks = client
    payload = {"username": "john"}

    mocks["user"].create_user.side_effect = ValueError("User already exists")

    response = client_app.post("/users/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    mocks["user"].create_user.assert_called_once()


def test_get_user_found(client, user_id):
    client_app, mocks = client
    mocks["user"].get_user.return_value = {"id":user_id, "username": "alice"}

    response = client_app.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"id":user_id, "username": "alice"}
    mocks["user"].get_user.assert_called_once_with(UUID(user_id))


def test_get_user_not_found(client, user_id):
    client_app, mocks = client
    mocks["user"].get_user.return_value = None

    response = client_app.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    mocks["user"].get_user.assert_called_once_with(UUID(user_id))


