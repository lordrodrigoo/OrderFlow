# pylint: disable=unused-argument
"""
Functional tests for the owner management journey.

Covers the full lifecycle of the system owner's role-management capabilities:
  - promoting a regular user to admin
  - verifying the promoted user gains admin access
  - demoting an admin back to user
  - verifying the demoted user loses admin access
  - security: owner cannot assign the owner role to anyone
  - security: non-owner cannot change anyone's role
"""


# ─────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────

def _register_user(client, suffix: str) -> dict:
    """Create and return a fresh regular user (returns the user JSON)."""
    payload = {
        "first_name": "Journey",
        "last_name": "User",
        "age": 25,
        "email": f"journey.{suffix}@owner.com",
        "phone": "11900000000",
        "password": "Journey@123",
        "username": f"journey.{suffix}",
        "role": "user",
    }
    resp = client.post("/api/v1/users/", json=payload)
    assert resp.status_code == 201, resp.json()
    return resp.json()


def _login_token(client, username: str, password: str = "Journey@123") -> dict:
    """Return auth headers for the given credentials."""
    resp = client.post("/api/v1/auth/", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.json()
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


# ─────────────────────────────────────────────────────────
# Promotion flow
# ─────────────────────────────────────────────────────────

def test_owner_promotes_user_to_admin(client, fake_user, fake_account, owner_auth_token):
    """
    Owner sends PATCH /users/{id}/role with role=admin.
    The response confirms the new role and subsequent admin requests succeed.
    """
    owner_headers = {"Authorization": f"Bearer {owner_auth_token}"}

    resp = client.patch(
        f"/api/v1/users/{fake_user.id}/role",
        json={"role": "admin"},
        headers=owner_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == "admin"


def test_promoted_user_can_access_admin_endpoints(client, owner_auth_token):
    """
    After being promoted to admin the user should be able to reach
    GET /admin/dashboard (admin-only endpoint) and receive 200.
    """
    owner_headers = {"Authorization": f"Bearer {owner_auth_token}"}

    # Create a fresh user and promote them
    user = _register_user(client, "promote1")
    client.patch(
        f"/api/v1/users/{user['id']}/role",
        json={"role": "admin"},
        headers=owner_headers,
    )

    # Login as the newly promoted admin
    admin_headers = _login_token(client, "journey.promote1")
    resp = client.get("/api/v1/admin/dashboard", headers=admin_headers)
    assert resp.status_code == 200


# ─────────────────────────────────────────────────────────
# Demotion flow
# ─────────────────────────────────────────────────────────

def test_owner_demotes_admin_to_user(client, fake_admin_user, fake_admin_account, owner_auth_token):
    """
    Owner sends PATCH /users/{id}/role with role=user for an existing admin.
    The response confirms the role was changed to user.
    """
    owner_headers = {"Authorization": f"Bearer {owner_auth_token}"}

    resp = client.patch(
        f"/api/v1/users/{fake_admin_user.id}/role",
        json={"role": "user"},
        headers=owner_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == "user"


def test_demoted_admin_loses_admin_access(client, owner_auth_token):
    """
    After demotion the former admin must receive 403 on admin-only endpoints.
    """
    owner_headers = {"Authorization": f"Bearer {owner_auth_token}"}

    # Register a user and promote to admin
    user = _register_user(client, "demote1")
    client.patch(
        f"/api/v1/users/{user['id']}/role",
        json={"role": "admin"},
        headers=owner_headers,
    )

    # Verify admin access granted
    promoted_headers = _login_token(client, "journey.demote1")
    resp = client.get("/api/v1/admin/dashboard", headers=promoted_headers)
    assert resp.status_code == 200

    # Demote back to user
    client.patch(
        f"/api/v1/users/{user['id']}/role",
        json={"role": "user"},
        headers=owner_headers,
    )

    # Must be rejected after demotion
    demoted_headers = _login_token(client, "journey.demote1")
    resp = client.get("/api/v1/admin/dashboard", headers=demoted_headers)
    assert resp.status_code == 403


# ─────────────────────────────────────────────────────────
# Security: owner role cannot be assigned
# ─────────────────────────────────────────────────────────

def test_owner_cannot_assign_owner_role_to_another_user(client, fake_user, fake_account, owner_auth_token):
    """
    Even the system owner is forbidden from assigning the owner role to anyone.
    Endpoint must return 403.
    """
    owner_headers = {"Authorization": f"Bearer {owner_auth_token}"}

    resp = client.patch(
        f"/api/v1/users/{fake_user.id}/role",
        json={"role": "owner"},
        headers=owner_headers,
    )
    assert resp.status_code == 403


# ─────────────────────────────────────────────────────────
# Security: non-owner cannot change roles
# ─────────────────────────────────────────────────────────

def test_regular_user_cannot_change_another_users_role(client, fake_user, owner_auth_token):
    """
    A regular user must receive 403 when attempting to change another user's role.
    """
    # Create a second user who will try to promote fake_user
    _register_user(client, "attacker1")
    attacker_headers = _login_token(client, "journey.attacker1")

    resp = client.patch(
        f"/api/v1/users/{fake_user.id}/role",
        json={"role": "admin"},
        headers=attacker_headers,
    )
    assert resp.status_code == 403


def test_admin_cannot_change_another_users_role(client, fake_user, fake_account, admin_auth_token):
    """
    Even a full admin must receive 403 when attempting to promote/demote another user.
    Only the owner has this privilege.
    """
    admin_headers = {"Authorization": f"Bearer {admin_auth_token}"}

    resp = client.patch(
        f"/api/v1/users/{fake_user.id}/role",
        json={"role": "user"},
        headers=admin_headers,
    )
    assert resp.status_code == 403


def test_unauthenticated_request_cannot_change_role(client, fake_user, fake_account):
    """
    Requests without a token are rejected with 401.
    """
    resp = client.patch(
        f"/api/v1/users/{fake_user.id}/role",
        json={"role": "admin"},
    )
    assert resp.status_code == 401
