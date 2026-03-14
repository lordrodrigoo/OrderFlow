
def test_login_success(client, user_login_data):
    response = client.post("/api/v1/accounts/login/", json=user_login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, fake_account):
    response = client.post("/api/v1/accounts/login/", json={
        "username": fake_account.username,
        "password": "WrongPassword123!"
    })
    assert response.status_code == 401


def test_login_invalid_username(client):
    response = client.post("/api/v1/accounts/login/", json={
        "username": "nonexistent_user",
        "password": "AnyPassword123!"
    })
    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post("/api/v1/accounts/login/", json={})
    assert response.status_code == 422


def test_refresh_token_success(client, user_login_data):
    login_response = client.post("/api/v1/accounts/login/", json=user_login_data)
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/api/v1/accounts/login/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post("/api/v1/accounts/login/refresh", json={
        "refresh_token": "invalid.token.value"
    })
    assert response.status_code == 401


def test_refresh_token_missing_field(client):
    response = client.post("/api/v1/accounts/login/refresh", json={})
    assert response.status_code == 422
