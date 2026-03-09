# pylint: disable=unused-argument

def test_create_product(client, fake_category, valid_product_data):
    response = client.post("/api/v1/products/", json=valid_product_data)
    assert response.status_code == 201


def test_get_product_by_id(client, fake_product):
    response = client.get(f"/api/v1/products/{fake_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_product.id


def test_get_inexistent_product_by_id(client):
    response = client.get("/api/v1/products/9999")
    assert response.status_code == 404


def test_list_products_without_filters(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1



def test_list_products_filter_by_name(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)

    response = client.get("/api/v1/products/", params={"name": valid_product_data["name"]})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == valid_product_data["name"]



def test_list_products_filter_by_category(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)

    response = client.get("/api/v1/products/", params={"category_id": valid_product_data["category_id"]})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["category_id"] == valid_product_data["category_id"]

def test_list_products_filter_by_availability(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)

    response = client.get("/api/v1/products/", params={"available": True})
    assert response.status_code == 200
    data = response.json()
    assert all(p["is_available"] for p in data)


def test_list_products_filter_by_price_range(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)

    response = client.get("/api/v1/products/", params={"min_price": 5.00, "max_price": 50.00})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for product in data:
        assert float(product["price"]) >= 5.00
        assert float(product["price"]) <= 50.00


def test_find_products_by_category(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)
    category_id = valid_product_data["category_id"]

    response = client.get(f"/api/v1/products/category/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(p["category_id"] == category_id for p in data)


def test_count_products_by_category(client, valid_product_data):
    client.post("/api/v1/products/", json=valid_product_data)
    category_id = valid_product_data["category_id"]

    response = client.get(f"/api/v1/products/count/category/{category_id}")
    assert response.status_code == 200
    assert response.json() >= 1


def test_update_product(client, valid_product_data):
    create_response = client.post("/api/v1/products/", json=valid_product_data)
    product_id = create_response.json()["id"]

    updated_data = valid_product_data.copy()
    updated_data["name"] = "Updated Product"
    updated_data["price"] = 29.99

    response = client.put(f"/api/v1/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert float(data["price"]) == 29.99


def test_delete_product(client, valid_product_data):
    create_response = client.post("/api/v1/products/", json=valid_product_data)
    product_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/products/{product_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 404
