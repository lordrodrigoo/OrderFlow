# pylint: disable=unused-argument

def test_update_order_status_as_admin(client, fake_order, admin_auth_token):
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "paid"},
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"


def test_update_order_status_forbidden_for_regular_user(client, fake_order, auth_token):
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "paid"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403


def test_update_order_status_unauthorized(client, fake_order):
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "paid"}
    )
    assert response.status_code == 401


def test_update_order_status_not_found(client, admin_auth_token):
    response = client.patch(
        "/api/v1/admin/orders/9999/status",
        json={"status": "paid"},
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 404


def test_update_order_status_invalid_status(client, fake_order, admin_auth_token):
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "invalid_status"},
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 422


def test_list_all_orders_as_admin(client, fake_order, admin_auth_token):
    response = client.get(
        "/api/v1/admin/orders",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(o["id"] == fake_order.id for o in data)


def test_list_all_orders_filter_by_status(client, fake_order, admin_auth_token):
    response = client.get(
        "/api/v1/admin/orders?order_status=pending",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert all(o["status"] == "pending" for o in data)


def test_list_all_orders_filter_by_user(client, fake_order, admin_auth_token):
    response = client.get(
        f"/api/v1/admin/orders?user_id={fake_order.user_id}",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert all(o["user_id"] == fake_order.user_id for o in data)


def test_list_all_orders_filter_by_amount(client, fake_order, admin_auth_token):
    response = client.get(
        "/api/v1/admin/orders?min_amount=100&max_amount=200",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert any(o["id"] == fake_order.id for o in data)
    assert all(100 <= float(o["total_amount"]) <= 200 for o in data)


def test_list_all_orders_filter_by_amount_no_match(client, fake_order, admin_auth_token):
    response = client.get(
        "/api/v1/admin/orders?min_amount=500&max_amount=1000",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert not any(o["id"] == fake_order.id for o in data)


def test_list_all_orders_forbidden_for_regular_user(client, auth_token):
    response = client.get(
        "/api/v1/admin/orders",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403


def test_list_all_orders_unauthorized(client):
    response = client.get("/api/v1/admin/orders")
    assert response.status_code == 401


def test_get_dashboard_as_admin(client, fake_order, fake_product, admin_auth_token):
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_orders" in data
    assert "total_users" in data
    assert "total_products" in data
    assert "total_revenue" in data
    assert "orders_by_status" in data
    assert data["total_orders"] >= 1
    assert data["total_products"] >= 1


def test_get_dashboard_forbidden_for_regular_user(client, auth_token):
    response = client.get(
        "/api/v1/admin/dashboard",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403


def test_get_dashboard_unauthorized(client):
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == 401
