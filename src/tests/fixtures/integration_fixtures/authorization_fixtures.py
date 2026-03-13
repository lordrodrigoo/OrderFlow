import pytest


@pytest.fixture
def auth_token(client, user_login_data):
    response = client.post("/api/v1/accounts/login", json=user_login_data)
    assert response.status_code == 200
    return response.json()["access_token"]
