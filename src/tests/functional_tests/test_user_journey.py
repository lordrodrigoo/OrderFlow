# pylint: disable=unused-argument
"""
Functional tests for the complete user journey.

Covers the full lifecycle of a regular user:
  - self-registration
  - adding and managing addresses
  - placing and canceling orders
  - security boundaries (cannot access other users' data)
"""
from datetime import datetime, timedelta
from decimal import Decimal


# ─────────────────────────────────────────────────────────
# Helper: register a brand-new user and return auth token
# ─────────────────────────────────────────────────────────

def _register_and_login(client, suffix: str) -> dict:
    """Register a fresh user and return (user_id, headers)."""
    payload = {
        "first_name": "User",
        "last_name": "Test",
        "age": 25,
        "email": f"user.{suffix}@journey.com",
        "phone": "11900000000",
        "password": "Journey@123",
        "username": f"user.{suffix}",
        "role": "user",
    }
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    auth = client.post("/api/v1/auth/", json={
        "username": f"user.{suffix}",
        "password": "Journey@123",
    })
    assert auth.status_code == 200
    token = auth.json()["access_token"]
    return user_id, {"Authorization": f"Bearer {token}"}


def _add_address(client, user_id: int, headers: dict) -> int:
    resp = client.post("/api/v1/users/me/addresses", json={
        "user_id": user_id,
        "street": "Journey Street",
        "number": "42",
        "complement": "Apt 1",
        "neighborhood": "Center",
        "city": "Sao Paulo",
        "state": "SP",
        "zip_code": "01310100",
        "is_default": True,
    }, headers=headers)
    assert resp.status_code == 201
    return resp.json()["id"]


def _place_order(client, address_id: int, headers: dict, amount: float = 100.00) -> dict:
    resp = client.post("/api/v1/orders/", json={
        "address_id": address_id,
        "total_amount": amount,
        "delivery_fee": 5.00,
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat(),
    }, headers=headers)
    assert resp.status_code == 201
    return resp.json()


# ─────────────────────────────────────────────────────────
# User self-registration
# ─────────────────────────────────────────────────────────

def test_new_user_is_created_with_role_user(client):
    """
    A newly registered user always gets role=user,
    regardless of what was sent in the request body.
    """
    resp = client.post("/api/v1/users/", json={
        "first_name": "Joao",
        "last_name": "Silva",
        "age": 22,
        "email": "joao.silva.journey@test.com",
        "phone": "11977777777",
        "password": "Journey@123",
        "username": "joao.silva.journey",
        "role": "admin",          # tries to self-promote
    })
    assert resp.status_code == 201
    assert resp.json()["role"] == "user"


def test_duplicate_email_is_rejected(client):
    """Registering with an already-used e-mail returns 409."""
    payload = {
        "first_name": "Maria",
        "last_name": "Souza",
        "age": 28,
        "email": "maria.dup@journey.com",
        "phone": "11966666666",
        "password": "Journey@123",
        "username": "maria.dup",
        "role": "user",
    }
    client.post("/api/v1/users/", json=payload)
    payload["username"] = "maria.dup2"
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code == 409


def test_duplicate_username_is_rejected(client):
    """Registering with an already-used username returns 409."""
    payload = {
        "first_name": "Pedro",
        "last_name": "Lima",
        "age": 30,
        "email": "pedro.lima1@journey.com",
        "phone": "11955555555",
        "password": "Journey@123",
        "username": "pedro.lima.dup",
        "role": "user",
    }
    client.post("/api/v1/users/", json=payload)
    payload["email"] = "pedro.lima2@journey.com"
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code == 409


# ─────────────────────────────────────────────────────────
# Address management
# ─────────────────────────────────────────────────────────

def test_user_registers_and_adds_address(client):
    """
    Full flow: register → login → add address → list addresses.
    The address must appear in /me/address.
    """
    user_id, headers = _register_and_login(client, "addr1")
    address_id = _add_address(client, user_id, headers)

    resp = client.get("/api/v1/users/me/address", headers=headers)
    assert resp.status_code == 200
    ids = [a["id"] for a in resp.json()]
    assert address_id in ids


def test_user_updates_own_address(client):
    """User can edit their own address."""
    user_id, headers = _register_and_login(client, "upd1")
    address_id = _add_address(client, user_id, headers)

    resp = client.put(f"/api/v1/users/me/addresses/{address_id}", json={
        "user_id": user_id,
        "street": "Updated Avenue",
        "number": "99",
        "complement": "Suite 3",
        "neighborhood": "Vila Nova",
        "city": "Campinas",
        "state": "SP",
        "zip_code": "13010100",
        "is_default": True,
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["street"] == "Updated Avenue"


def test_user_sets_default_address(client):
    """User can mark an address as default."""
    user_id, headers = _register_and_login(client, "def1")
    address_id = _add_address(client, user_id, headers)

    resp = client.patch(
        f"/api/v1/users/me/addresses/{address_id}/default",
        headers=headers
    )
    assert resp.status_code == 200
    assert resp.json()["is_default"] is True


# ─────────────────────────────────────────────────────────
# Placing orders
# ─────────────────────────────────────────────────────────

def test_user_places_order_and_adds_item(client, fake_product):
    """
    User registers, adds an address, places an order,
    and adds a product item to it.
    """
    user_id, headers = _register_and_login(client, "order1")
    address_id = _add_address(client, user_id, headers)
    order = _place_order(client, address_id, headers)
    order_id = order["id"]

    # Add an item to the order
    unit_price = float(Decimal(str(fake_product.price)))
    resp = client.post("/api/v1/order-items/", json={
        "order_id": order_id,
        "product_id": fake_product.id,
        "quantity": 2,
        "unit_price": unit_price,
        "subtotal": round(unit_price * 2, 2),
        "notes": "No onions",
    }, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["product_id"] == fake_product.id


def test_user_views_own_order(client):
    """User can retrieve their own orders by ID and in the listing."""
    user_id, headers = _register_and_login(client, "view1")
    address_id = _add_address(client, user_id, headers)
    order_id = _place_order(client, address_id, headers)["id"]

    # By ID
    resp = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == order_id

    # In listing
    resp = client.get("/api/v1/orders/", headers=headers)
    assert any(o["id"] == order_id for o in resp.json())


def test_user_cancels_own_order(client):
    """User can cancel their own pending order."""
    user_id, headers = _register_and_login(client, "cancel1")
    address_id = _add_address(client, user_id, headers)
    order_id = _place_order(client, address_id, headers)["id"]

    resp = client.post(f"/api/v1/orders/{order_id}/cancel", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "canceled"


# ─────────────────────────────────────────────────────────
# Security boundaries
# ─────────────────────────────────────────────────────────

def test_user_cannot_view_another_users_order(client):
    """A user must not see orders that belong to another user."""
    user_id_a, headers_a = _register_and_login(client, "sec1a")
    _, headers_b = _register_and_login(client, "sec1b")

    address_id = _add_address(client, user_id_a, headers_a)
    order_id = _place_order(client, address_id, headers_a)["id"]

    resp = client.get(f"/api/v1/orders/{order_id}", headers=headers_b)
    assert resp.status_code == 404


def test_unauthenticated_user_cannot_place_order(client, fake_address):
    """Requests without a token are rejected with 401."""
    resp = client.post("/api/v1/orders/", json={
        "address_id": fake_address.id,
        "total_amount": 50.00,
        "delivery_fee": 5.00,
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat(),
    })
    assert resp.status_code == 401


def test_token_gives_access_to_own_profile(client):
    """Authenticated user can see their own profile via /me."""
    _, headers = _register_and_login(client, "me1")
    resp = client.get("/api/v1/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "user.me1@journey.com"
