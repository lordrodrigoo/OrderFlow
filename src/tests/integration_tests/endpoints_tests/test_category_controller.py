# pylint: disable=unused-argument
def test_create_category(client, valid_category_data, admin_auth_token):
    response = client.post("/api/v1/categories/", json=valid_category_data,
                           headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == valid_category_data["name"]
    assert data["description"] == valid_category_data["description"]


def test_create_category_forbidden_for_regular_user(client, valid_category_data, auth_token):
    response = client.post("/api/v1/categories/", json=valid_category_data,
                           headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403


def test_create_category_unauthorized(client, valid_category_data):
    response = client.post("/api/v1/categories/", json=valid_category_data)
    assert response.status_code == 401



def test_get_category_by_id(client, fake_category):
    response = client.get(f"/api/v1/categories/{fake_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_category.id
    assert data["name"] == fake_category.name



def test_get_inexistent_category_by_id(client):
    response = client.get("/api/v1/categories/9999")
    assert response.status_code == 404



def test_list_categories(client, fake_category):
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1



def test_update_category(client, fake_category, valid_category_data, admin_auth_token):
    updated_data = valid_category_data.copy()
    updated_data["name"] = "Updated Cat"
    updated_data["description"] = "Updated description here"

    response = client.put(f"/api/v1/categories/{fake_category.id}", json=updated_data,
                          headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Cat"
    assert data["description"] == "Updated description here"


def test_update_category_forbidden_for_regular_user(client, fake_category, valid_category_data, auth_token):
    response = client.put(f"/api/v1/categories/{fake_category.id}", json=valid_category_data,
                          headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403



def test_delete_category(client, fake_category, admin_auth_token):
    delete_response = client.delete(f"/api/v1/categories/{fake_category.id}",
                                    headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/categories/{fake_category.id}")
    assert get_response.status_code == 404


def test_delete_category_forbidden_for_regular_user(client, fake_category, auth_token):
    response = client.delete(f"/api/v1/categories/{fake_category.id}",
                             headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403



def test_create_category_without_description(client, admin_auth_token):
    response = client.post("/api/v1/categories/", json={"name": "Drinks"},
                           headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Drinks"
    assert data["description"] is None


def test_create_category_with_invalid_name(client, admin_auth_token):
    response = client.post("/api/v1/categories/", json={
        "name": "@@Invalid!!",
        "description": "Some valid description here"
    }, headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 422
