#pylint: disable=unused-argument
def test_create_user(client, valid_user_data):
    response = client.post("/api/v1/users/", json=valid_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == valid_user_data["email"]


def test_list_users_with_filters(client, valid_user_data):
    client.post("/api/v1/users/", json=valid_user_data)

    response = client.get(
        "/api/v1/users/",
        params={
            "email": valid_user_data["email"]})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == valid_user_data["email"]


def test_list_users_with_name_filter(client, fake_user, fake_account):
    response = client.get("/api/v1/users/", params={"name": fake_user.first_name})
    assert response.status_code == 200
    data = response.json()
    assert any(u["email"] == fake_user.email for u in data)


def test_list_users_with_active_filter(client, fake_user, fake_account):
    response = client.get("/api/v1/users/", params={"active": True})
    assert response.status_code == 200
    data = response.json()
    assert all(u["is_active"] is True for u in data)


def test_list_users_without_filters(client, valid_user_data):
    client.post("/api/v1/users/", json=valid_user_data)

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_user_by_id(client, valid_user_data):
    create_response = client.post("/api/v1/users/", json = valid_user_data)
    user_id = create_response.json()["id"]
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id


def test_get_inexistent_user_by_id(client):
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404


def test_get_me(client, auth_token):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data


def test_add_address(client, auth_token, fake_user):
    address_data = {
        "user_id": fake_user.id,
        "street": "Test Street",
        "number": "100",
        "complement": "Apt 1",
        "neighborhood": "Center",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01310100",
        "is_default": False
    }
    response = client.post(
        "/api/v1/users/me/addresses",
        json=address_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201


def test_list_my_addresses(client, auth_token, fake_address):
    response = client.get(
        "/api/v1/users/me/address",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_user(client, auth_token, fake_user):
    update_data = {
        "first_name": "Ana",
        "last_name": "Silva",
        "age": 29,
        "email": fake_user.email,
        "phone": "11999999999",
        "password": "StrongPassword123!",
        "username": "ana_silva",
        "role": "user"
    }
    response = client.put(
        f"/api/v1/users/{fake_user.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Ana"


def test_update_me(client, auth_token, fake_user):
    update_data = {
        "first_name": "Ana",
        "last_name": "Silva",
        "age": 28,
        "email": fake_user.email,
        "phone": "11999999999",
        "password": "StrongPassword123!",
        "username": "ana_silva",
        "role": "user"
    }
    response = client.put(
        "/api/v1/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_update_address(client, auth_token, fake_address):
    address_data = {
        "user_id": fake_address.user_id,
        "street": "Updated Street",
        "number": "200",
        "complement": "Apt 2",
        "neighborhood": "New Center",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01310100",
        "is_default": True
    }
    response = client.put(
        f"/api/v1/users/me/addresses/{fake_address.id}",
        json=address_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_set_default_address(client, auth_token, fake_address):
    response = client.patch(
        f"/api/v1/users/me/addresses/{fake_address.id}/default",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_delete_user(client, valid_user_data):
    create_response = client.post("/api/v1/users/", json=valid_user_data)
    user_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
