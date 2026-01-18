from uuid import UUID

def test_create_location(client, location_id):
    client_app, mocks = client
    payload = {
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }
    mocks["location"].create_location.return_value = {
        "id":location_id,
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }

    response = client_app.post("/locations/", json=payload)
    assert response.status_code == 200
    assert response.json() == mocks["location"].create_location.return_value

def test_get_location_found(client, location_id):
    client_app, mocks = client
    mocks["location"].get_location.return_value = {
        "id":location_id,
        "name": "Box A",
        "address": "123 Street",
        "location_type": "CrossFit Box"
    }

    response = client_app.get(f"/locations/{location_id}")
    assert response.status_code == 200
    assert response.json() == mocks["location"].get_location.return_value


def test_get_location_not_found(client, location_id):
    client_app, mocks = client
    mocks["location"].get_location.return_value = None

    response = client_app.get(f"/locations/{location_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

def test_list_locations(client, location_id):
    client_app, mocks = client
    mocks["location"].list_locations.return_value = [
        {"id":location_id, "name": "Box A", "address": "123 Street", "location_type": "CrossFit Box"},
        {"id":location_id, "name": "Box B", "address": None, "location_type": "Gym"}
    ]

    response = client_app.get("/locations/")
    assert response.status_code == 200
    assert response.json() == mocks["location"].list_locations.return_value

def test_delete_location_success(client, location_id):
    client_app, mocks = client

    response = client_app.delete(f"/locations/{location_id}")
    assert response.status_code == 204
    mocks["location"].delete_location.assert_called_once_with(UUID(location_id))


def test_delete_location_not_found(client, location_id):
    client_app, mocks = client
    mocks["location"].delete_location.side_effect = ValueError("Location not found")

    response = client_app.delete(f"/locations/{location_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Location not found"

