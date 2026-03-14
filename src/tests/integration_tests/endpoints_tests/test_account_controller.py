def test_create_account(client, valid_account_data):
    response = client.post("/api/v1/accounts/", json=valid_account_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == valid_account_data["username"]
    assert data["status"] == "active"


def test_create_account_duplicate_username(client, fake_account, valid_account_data):
    valid_account_data["username"] = fake_account.username
    response = client.post("/api/v1/accounts/", json=valid_account_data)
    assert response.status_code == 409


def test_get_account_by_id(client, fake_account, auth_token):
    response = client.get(
        f"/api/v1/accounts/{fake_account.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_account.id


def test_get_account_not_found(client, auth_token):
    response = client.get(
        "/api/v1/accounts/9999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404


def test_update_account(client, fake_account, auth_token):
    response = client.put(
        f"/api/v1/accounts/{fake_account.id}",
        json={"username": "ana_updated"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "ana_updated"


def test_update_password(client, fake_account, auth_token):
    response = client.patch(
        f"/api/v1/accounts/{fake_account.id}/password",
        json={
            "current_password": "StrongPassword123!",
            "new_password": "NewStr0ng@Pass"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_deactivate_account(client, fake_account, auth_token):
    response = client.patch(
        f"/api/v1/accounts/{fake_account.id}/deactivate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_suspend_account(client, fake_account, auth_token):
    response = client.patch(
        f"/api/v1/accounts/{fake_account.id}/suspended",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "suspended"


def test_activate_account(client, fake_account, auth_token):
    response = client.patch(
        f"/api/v1/accounts/{fake_account.id}/activate",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_inactivate_account(client, fake_account, auth_token):
    response = client.patch(
        f"/api/v1/accounts/{fake_account.id}/inactive",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"


def test_delete_account(client, fake_account, auth_token):
    response = client.delete(
        f"/api/v1/accounts/{fake_account.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/accounts/{fake_account.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404
