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


def test_update_user():
    # This test will be implemented after authentication and authorization.
    pass


def test_delete_user(client, valid_user_data):
    create_response = client.post("/api/v1/users/", json=valid_user_data)
    user_id = create_response.json()["id"]
    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
