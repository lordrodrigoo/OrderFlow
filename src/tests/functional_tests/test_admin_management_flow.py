# pylint: disable=unused-argument
"""
Functional tests for admin management flows.

These tests simulate complete admin journeys across multiple endpoints,
verifying cross-cutting concerns like status progression, revenue accuracy,
and order filtering from an admin perspective.
"""
from src.tests.functional_tests.helpers import create_order as _create_order


def test_admin_advances_order_through_statuses(client, fake_order, auth_token, admin_auth_token):
    """
    Admin advances an order through the full status progression:
    pending → paid → delivered. The user sees the updated status at each step.
    """
    admin_headers = {"Authorization": f"Bearer {admin_auth_token}"}
    user_headers = {"Authorization": f"Bearer {auth_token}"}

    # Confirm initial state
    response = client.get(f"/api/v1/orders/{fake_order.id}", headers=user_headers)
    assert response.json()["status"] == "pending"

    # Admin advances to paid
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "paid"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "paid"

    # Admin advances to delivered
    response = client.patch(
        f"/api/v1/admin/orders/{fake_order.id}/status",
        json={"status": "delivered"},
        headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "delivered"

    # User confirms the final status reflects the admin changes
    response = client.get(f"/api/v1/orders/{fake_order.id}", headers=user_headers)
    assert response.json()["status"] == "delivered"


def test_dashboard_reflects_platform_state(client, fake_order, fake_product, admin_auth_token):
    """
    Dashboard stats accurately reflect the current state of the platform:
    known orders, products, and users are counted, and pending orders
    appear in the status breakdown.
    """
    admin_headers = {"Authorization": f"Bearer {admin_auth_token}"}

    response = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()

    assert data["total_orders"] >= 1
    assert data["total_products"] >= 1
    assert data["total_users"] >= 1
    assert data["total_revenue"] > 0
    assert "pending" in data["orders_by_status"]
    assert data["orders_by_status"]["pending"] >= 1


def test_canceled_orders_excluded_from_dashboard_revenue(client, fake_address, auth_token, admin_auth_token):
    """
    Revenue in the dashboard excludes canceled orders.
    Canceling an order reduces the reported revenue by exactly its total amount.
    """
    user_headers = {"Authorization": f"Bearer {auth_token}"}
    admin_headers = {"Authorization": f"Bearer {admin_auth_token}"}

    order_id = _create_order(client, fake_address.id, 500.00, user_headers, delivery_fee=10.00)["id"]

    # Revenue must include the newly created order
    response = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    revenue_before = response.json()["total_revenue"]
    assert revenue_before >= 500.00

    # Cancel the order
    client.post(f"/api/v1/orders/{order_id}/cancel", headers=user_headers)

    # Revenue must drop by exactly the canceled order's amount
    response = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    revenue_after = response.json()["total_revenue"]
    assert revenue_after == revenue_before - 500.00


def test_admin_filters_orders_by_amount_range(client, fake_address, auth_token, admin_auth_token):
    """
    Admin can filter all orders by a monetary range,
    returning only the orders whose total_amount falls within [min, max].
    """
    user_headers = {"Authorization": f"Bearer {auth_token}"}
    admin_headers = {"Authorization": f"Bearer {admin_auth_token}"}

    low_id = _create_order(client, fake_address.id, 75.00, user_headers)["id"]
    high_id = _create_order(client, fake_address.id, 600.00, user_headers)["id"]

    response = client.get("/api/v1/admin/orders?min_amount=50&max_amount=100", headers=admin_headers)
    assert response.status_code == 200

    result_ids = [o["id"] for o in response.json()]
    assert low_id in result_ids
    assert high_id not in result_ids
