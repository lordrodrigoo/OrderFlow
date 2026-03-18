# pylint: disable=unused-argument

def test_create_product(client, fake_category, valid_product_data, admin_auth_token):
    response = client.post("/api/v1/products/", json=valid_product_data,
                           headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 201


def test_create_product_forbidden_for_regular_user(client, fake_category, valid_product_data, auth_token):
    response = client.post("/api/v1/products/", json=valid_product_data,
                           headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403


def test_create_product_unauthorized(client, fake_category, valid_product_data):
    response = client.post("/api/v1/products/", json=valid_product_data)
    assert response.status_code == 401


def test_get_product_by_id(client, fake_product):
    response = client.get(f"/api/v1/products/{fake_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_product.id


def test_get_inexistent_product_by_id(client):
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404


def test_list_products_without_filters(client, fake_product, valid_product_data):
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1



def test_list_products_filter_by_name(client, fake_product):
    response = client.get("/api/v1/products/", params={"name": fake_product.name})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == fake_product.name



def test_list_products_filter_by_category(client, fake_product):
    response = client.get("/api/v1/products/", params={"category_id": fake_product.category_id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["category_id"] == fake_product.category_id

def test_list_products_filter_by_availability(client, fake_product):
    response = client.get("/api/v1/products/", params={"available": True})
    assert response.status_code == 200
    data = response.json()
    assert all(p["is_available"] for p in data)


def test_list_products_filter_by_price_range(client, fake_product, valid_product_data):
    response = client.get("/api/v1/products/", params={"min_price": 5.00, "max_price": 50.00})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for product in data:
        assert float(product["price"]) >= 5.00
        assert float(product["price"]) <= 50.00


def test_find_products_by_category(client, fake_product):
    response = client.get(f"/api/v1/products/category/{fake_product.category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(p["category_id"] == fake_product.category_id for p in data)


def test_count_products_by_category(client, fake_product):
    response = client.get(f"/api/v1/products/count/category/{fake_product.category_id}")
    assert response.status_code == 200
    assert response.json() >= 1


def test_update_product(client, fake_product, valid_product_data, admin_auth_token):
    updated_data = valid_product_data.copy()
    updated_data["name"] = "Updated Product"
    updated_data["price"] = 29.99

    response = client.put(f"/api/v1/products/{fake_product.id}", json=updated_data,
                          headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert float(data["price"]) == 29.99


def test_update_product_forbidden_for_regular_user(client, fake_product, valid_product_data, auth_token):
    response = client.put(f"/api/v1/products/{fake_product.id}", json=valid_product_data,
                          headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403


def test_delete_product(client, fake_product, admin_auth_token):
    delete_response = client.delete(f"/api/v1/products/{fake_product.id}",
                                    headers={"Authorization": f"Bearer {admin_auth_token}"})
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/products/{fake_product.id}")
    assert get_response.status_code == 404


def test_delete_product_forbidden_for_regular_user(client, fake_product, auth_token):
    response = client.delete(f"/api/v1/products/{fake_product.id}",
                             headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 403
