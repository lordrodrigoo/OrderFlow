# pylint: disable=unused-argument
"""
Functional tests for order lifecycle.

These tests simulate complete user journeys across multiple endpoints,
verifying that the system behaves correctly end-to-end for real usage scenarios.
"""
from src.tests.functional_tests.helpers import create_order as _create_order


def test_complete_order_flow(client, fake_address, auth_token):
    """
    User creates an order, retrieves it by ID, sees it in their list,
    cancels it, and verifies it appears under the 'canceled' filter.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Step 1: Create the order
    order = _create_order(client, fake_address.id, 99.90, headers)
    order_id = order["id"]
    assert order["status"] == "pending"

    # Step 2: Retrieve by ID
    response = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == order_id

    # Step 3: Appears in the user's order listing
    response = client.get("/api/v1/orders/", headers=headers)
    assert response.status_code == 200
    assert any(o["id"] == order_id for o in response.json())

    # Step 4: Cancel the order
    response = client.post(f"/api/v1/orders/{order_id}/cancel", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "canceled"

    # Step 5: Appears when filtering by 'canceled' status
    response = client.get("/api/v1/orders/?order_status=canceled", headers=headers)
    assert response.status_code == 200
    assert any(o["id"] == order_id for o in response.json())


def test_cannot_cancel_already_canceled_order(client, fake_address, auth_token):
    """
    Attempting to cancel an order that is already canceled returns 409 Conflict.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    order_id = _create_order(client, fake_address.id, 50.00, headers)["id"]

    client.post(f"/api/v1/orders/{order_id}/cancel", headers=headers)

    response = client.post(f"/api/v1/orders/{order_id}/cancel", headers=headers)
    assert response.status_code == 409


def test_user_cannot_access_another_users_order(client, fake_order):
    """
    A user cannot read or cancel an order that belongs to a different user.
    Both operations must return 404 to avoid exposing order existence.
    """
    # Register a second, independent user (account is created alongside)
    user_response = client.post("/api/v1/users/", json={
        "first_name": "Carlos", "last_name": "Lima", "age": 25,
        "email": "carlos.lima@example.com", "phone": "11888888888",
        "password": "SecurePass456!", "username": "carlos.lima",
        "role": "user"
    })
    assert user_response.status_code == 201

    auth_response = client.post("/api/v1/auth/", json={
        "username": "carlos.lima",
        "password": "SecurePass456!"
    })
    assert auth_response.status_code == 200
    other_headers = {"Authorization": f"Bearer {auth_response.json()['access_token']}"}

    # Second user tries to read first user's order
    response = client.get(f"/api/v1/orders/{fake_order.id}", headers=other_headers)
    assert response.status_code == 404

    # Second user tries to cancel first user's order
    response = client.post(f"/api/v1/orders/{fake_order.id}/cancel", headers=other_headers)
    assert response.status_code == 404


def test_order_amount_filter_scoped_to_user(client, fake_address, auth_token):
    """
    When filtering by amount range, only the current user's orders
    that fall within the range are returned.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}

    cheap_id = _create_order(client, fake_address.id, 30.00, headers)["id"]
    expensive_id = _create_order(client, fake_address.id, 250.00, headers)["id"]

    response = client.get("/api/v1/orders/?min_amount=20&max_amount=100", headers=headers)
    assert response.status_code == 200

    result_ids = [o["id"] for o in response.json()]
    assert cheap_id in result_ids
    assert expensive_id not in result_ids
