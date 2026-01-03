


def test_create_user_success(client_app):
    payload = {"username": "john"}
    response = client_app.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "john"
    assert "id" in data

def test_create_user_duplicate(client_app):
    payload = {"username": "john"}
    client_app.post("/users/", json=payload)  # crée l'utilisateur
    response = client_app.post("/users/", json=payload)  # essai de créer le même
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_get_user_not_found(client_app):
    response = client_app.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

