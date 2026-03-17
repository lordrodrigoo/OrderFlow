
def test_login_success(client, user_login_data):
    response = client.post("/api/v1/auth/", json=user_login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, fake_account):
    response = client.post("/api/v1/auth/", json={
        "username": fake_account.username,
        "password": "WrongPassword123!"
    })
    assert response.status_code == 401


def test_login_invalid_username(client):
    response = client.post("/api/v1/auth/", json={
        "username": "nonexistent_user",
        "password": "AnyPassword123!"
    })
    assert response.status_code == 401


def test_login_missing_fields(client):
    response = client.post("/api/v1/auth/", json={})
    assert response.status_code == 422


def test_refresh_token_success(client, user_login_data):
    login_response = client.post("/api/v1/auth/", json=user_login_data)
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post("/api/v1/auth/refresh", json={
        "refresh_token": "invalid.token.value"
    })
    assert response.status_code == 401


def test_refresh_token_missing_field(client):
    response = client.post("/api/v1/auth/refresh", json={})
    assert response.status_code == 422


# ─── Rate Limiting ─────────────────────────────────────────────────────────────

def test_login_rate_limit_exceeded(client):
    """Should return 429 after exceeding 5 requests per minute on /login."""
    payload = {"username": "any_user", "password": "AnyPassword123!"}
    for _ in range(5):
        client.post("/api/v1/auth/", json=payload)

    response = client.post("/api/v1/auth/", json=payload)
    assert response.status_code == 429
