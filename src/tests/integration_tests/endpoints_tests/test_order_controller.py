#pylint: disable=unused-argument
def test_create_order(client, auth_token, valid_order_data):
    response = client.post("/api/v1/orders/", json=valid_order_data,
                           headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["address_id"] == valid_order_data["address_id"]
    assert data["status"] == "pending"


def test_create_order_missing_fields(client, auth_token):
    response = client.post("/api/v1/orders/", json={},
                           headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 422


def test_get_order_by_id(client, fake_order):
    response = client.get(f"/api/v1/orders/{fake_order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_order.id


def test_get_order_not_found(client):
    response = client.get("/api/v1/orders/9999")
    assert response.status_code == 404


def test_list_orders_no_filter(client, fake_order):
    response = client.get("/api/v1/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(o["id"] == fake_order.id for o in data)


def test_list_orders_filter_by_user(client, fake_order):
    response = client.get(f"/api/v1/orders/?user_id={fake_order.user_id}")
    assert response.status_code == 200
    data = response.json()
    assert all(o["user_id"] == fake_order.user_id for o in data)


def test_list_orders_filter_by_status(client, fake_order):
    response = client.get("/api/v1/orders/?order_status=pending")
    assert response.status_code == 200
    data = response.json()
    assert all(o["status"] == "pending" for o in data)


def test_list_orders_filter_by_amount(client, fake_order):
    response = client.get("/api/v1/orders/?min_amount=100&max_amount=200")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_order(client, fake_order, valid_order_data):
    response = client.put(f"/api/v1/orders/{fake_order.id}", json=valid_order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == fake_order.id


def test_update_order_not_found(client, valid_order_data):
    response = client.put("/api/v1/orders/9999", json=valid_order_data)
    assert response.status_code == 404


def test_cancel_order(client, fake_order):
    response = client.post(f"/api/v1/orders/{fake_order.id}/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "canceled"


def test_cancel_order_already_canceled(client, fake_order):
    client.post(f"/api/v1/orders/{fake_order.id}/cancel")
    response = client.post(f"/api/v1/orders/{fake_order.id}/cancel")
    assert response.status_code == 409


def test_delete_order(client, fake_order):
    response = client.delete(f"/api/v1/orders/{fake_order.id}")
    assert response.status_code == 204
    get_response = client.get(f"/api/v1/orders/{fake_order.id}")
    assert get_response.status_code == 404


def test_delete_order_not_found(client):
    response = client.delete("/api/v1/orders/9999")
    assert response.status_code == 404
