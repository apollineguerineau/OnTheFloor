def test_create_location(client):
    client_app, mocks = client
    payload = {
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }
    mocks["location"].create_location.return_value = {
        "id": 1,
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }

    response = client_app.post("/locations/", json=payload)
    assert response.status_code == 200
    assert response.json() == mocks["location"].create_location.return_value

def test_get_location_found(client):
    client_app, mocks = client
    mocks["location"].get_location.return_value = {
        "id": 1,
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }

    response = client_app.get("/locations/1")
    assert response.status_code == 200
    assert response.json() == mocks["location"].get_location.return_value


def test_get_location_not_found(client):
    client_app, mocks = client
    mocks["location"].get_location.return_value = None

    response = client_app.get("/locations/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

def test_list_locations(client):
    client_app, mocks = client
    mocks["location"].list_locations.return_value = [
        {"id": 1, "name": "Box A", "address": "123 Street", "location_type": "CrossFit Box"},
        {"id": 2, "name": "Box B", "address": None, "location_type": "Gym"}
    ]

    response = client_app.get("/locations/")
    assert response.status_code == 200
    assert response.json() == mocks["location"].list_locations.return_value

def test_delete_location_success(client):
    client_app, mocks = client

    response = client_app.delete("/locations/1")
    assert response.status_code == 204
    mocks["location"].delete_location.assert_called_once_with(1)


def test_delete_location_not_found(client):
    client_app, mocks = client
    mocks["location"].delete_location.side_effect = ValueError("Location not found")

    response = client_app.delete("/locations/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

