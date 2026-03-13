def test_create_address(client, valid_address_data, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/api/v1/addresses/",
        json=valid_address_data,
        headers=headers
    )
    assert response.status_code == 201


def test_find_all_addresses(client, valid_address_data):
    client.post("/api/v1/addresses/", json=valid_address_data)

    response = client.get("/api/v1/addresses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_find_address_by_id(client, valid_address_data):
    create_response = client.post("/api/v1/addresses/", json=valid_address_data)
    address_id = create_response.json()["id"]

    response = client.get(f"/api/v1/addresses/{address_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == address_id


def test_update_address():
    # This test will be implemented after authentication and authorization.
    pass


def test_delete_address(client, valid_address_data):
    create_response = client.post("/api/v1/addresses/", json=valid_address_data)
    address_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/addresses/{address_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/addresses/{address_id}")
    assert get_response.status_code == 404


def test_find_addresses_by_user_id(client, valid_address_data):
    client.post("/api/v1/addresses/", json=valid_address_data)
    user_id = valid_address_data["user_id"]

    response = client.get(f"/api/v1/addresses/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["user_id"] == user_id
