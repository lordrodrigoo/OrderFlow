#pylint: disable=unused-argument
def test_create_order_item(client, valid_order_item_data):
    response = client.post("/api/v1/order-items/", json=valid_order_item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == valid_order_item_data["order_id"]
    assert data["product_id"] == valid_order_item_data["product_id"]
    assert data["quantity"] == valid_order_item_data["quantity"]


def test_create_order_item_order_not_found(client, fake_product):
    response = client.post("/api/v1/order-items/", json={
        "order_id": 9999,
        "product_id": fake_product.id,
        "quantity": 1,
        "unit_price": "10.00"
    })
    assert response.status_code == 404


def test_create_order_item_product_not_found(client, fake_order):
    response = client.post("/api/v1/order-items/", json={
        "order_id": fake_order.id,
        "product_id": 9999,
        "quantity": 1,
        "unit_price": "10.00"
    })
    assert response.status_code == 404


def test_create_order_item_duplicate(client, fake_order_item, valid_order_item_data):
    response = client.post("/api/v1/order-items/", json=valid_order_item_data)
    assert response.status_code == 400


def test_get_order_item_by_id(client, fake_order_item):
    response = client.get(f"/api/v1/order-items/{fake_order_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_order_item.id


def test_get_order_item_not_found(client):
    response = client.get("/api/v1/order-items/9999")
    assert response.status_code == 404


def test_list_order_items_no_filter(client, fake_order_item):
    response = client.get("/api/v1/order-items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_list_order_items_filter_by_order(client, fake_order_item):
    response = client.get("/api/v1/order-items/", params={"order_id": fake_order_item.order_id})
    assert response.status_code == 200
    data = response.json()
    assert all(item["order_id"] == fake_order_item.order_id for item in data)


def test_list_order_items_order_not_found(client):
    response = client.get("/api/v1/order-items/", params={"order_id": 9999})
    assert response.status_code == 404


def test_update_order_item(client, fake_order_item):
    response = client.put(f"/api/v1/order-items/{fake_order_item.id}", json={
        "order_id": fake_order_item.order_id,
        "product_id": fake_order_item.product_id,
        "quantity": 5,
        "unit_price": "30.00"
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 5


def test_update_order_item_not_found(client, fake_order, fake_product):
    response = client.put("/api/v1/order-items/9999", json={
        "order_id": fake_order.id,
        "product_id": fake_product.id,
        "quantity": 1,
        "unit_price": "10.00"
    })
    assert response.status_code == 404


def test_delete_order_item(client, fake_order_item):
    delete_response = client.delete(f"/api/v1/order-items/{fake_order_item.id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/order-items/{fake_order_item.id}")
    assert get_response.status_code == 404
