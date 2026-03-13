def test_create_address(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/api/v1/addresses/",
        json=valid_address_data,
        headers=headers
    )
    assert response.status_code == 201


def test_find_all_addresses(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/api/v1/addresses/", json=valid_address_data, headers=headers)

    response = client.get("/api/v1/addresses/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_find_address_by_id(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = client.post("/api/v1/addresses/", json=valid_address_data, headers=headers)
    address_id = create_response.json()["id"]

    response = client.get(f"/api/v1/addresses/{address_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == address_id


def test_update_address(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = client.post("/api/v1/addresses/", json=valid_address_data, headers=headers)
    address_id = create_response.json()["id"]

    updated_data = valid_address_data.copy()
    updated_data["street"] = "Updated Street"

    update_response = client.put(f"/api/v1/addresses/{address_id}", json=updated_data, headers=headers)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["street"] == "Updated Street"


def test_delete_address(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = client.post("/api/v1/addresses/", json=valid_address_data, headers=headers)
    address_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/addresses/{address_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/addresses/{address_id}", headers=headers)
    assert get_response.status_code == 404


def test_find_addresses_by_user_id(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/api/v1/addresses/", json=valid_address_data, headers=headers)
    user_id = valid_address_data["user_id"]

    response = client.get(f"/api/v1/addresses/user/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["user_id"] == user_id
