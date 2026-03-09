def test_create_category(client, valid_category_data):
    response = client.post("/api/v1/categories/", json=valid_category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == valid_category_data["name"]
    assert data["description"] == valid_category_data["description"]



def test_get_category_by_id(client, valid_category_data):
    create_response = client.post("/api/v1/categories/", json=valid_category_data)
    category_id = create_response.json()["id"]

    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == valid_category_data["name"]



def test_get_inexistent_category_by_id(client):
    response = client.get("/api/v1/categories/9999")
    assert response.status_code == 404



def test_list_categories(client, valid_category_data):
    client.post("/api/v1/categories/", json=valid_category_data)

    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1



def test_update_category(client, valid_category_data):
    create_response = client.post("/api/v1/categories/", json=valid_category_data)
    category_id = create_response.json()["id"]

    updated_data = valid_category_data.copy()
    updated_data["name"] = "Updated Cat"
    updated_data["description"] = "Updated description here"

    response = client.put(f"/api/v1/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Cat"
    assert data["description"] == "Updated description here"



def test_delete_category(client, valid_category_data):
    create_response = client.post("/api/v1/categories/", json=valid_category_data)
    category_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/categories/{category_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == 404



def test_create_category_without_description(client):
    response = client.post("/api/v1/categories/", json={"name": "Drinks"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Drinks"
    assert data["description"] is None



def test_create_category_with_invalid_name(client):
    response = client.post("/api/v1/categories/", json={
        "name": "@@Invalid!!",
        "description": "Some valid description here"
    })
    assert response.status_code == 422
