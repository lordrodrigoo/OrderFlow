#pylint: disable=redefined-outer-name
from datetime import datetime
import pytest
from src.infra.db.entities.user import UserEntity
from src.infra.db.entities.account import AccountEntity
from src.config.security import hash_password


@pytest.fixture
def fake_admin_user(db_session):
    user = UserEntity(
        first_name="Admin",
        last_name="User",
        age=30,
        email="admin@orderflow.com",
        phone="11000000000",
        is_active=True,
        role="admin",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def fake_admin_account(db_session, fake_admin_user):
    account = AccountEntity(
        user_id=fake_admin_user.id,
        username="admin_orderflow",
        password_hash=hash_password("AdminPass123!"),
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(account)
    db_session.commit()
    return account


@pytest.fixture
def admin_auth_token(client, fake_admin_account):
    response = client.post("/api/v1/auth/", json={
        "username": fake_admin_account.username,
        "password": "AdminPass123!"
    })
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def fake_owner_user(db_session):
    user = UserEntity(
        first_name="System",
        last_name="Owner",
        age=30,
        email="owner@orderflow.com",
        phone="11000000001",
        is_active=True,
        role="owner",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def fake_owner_account(db_session, fake_owner_user):
    account = AccountEntity(
        user_id=fake_owner_user.id,
        username="owner_orderflow",
        password_hash=hash_password("OwnerPass123!"),
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(account)
    db_session.commit()
    return account


@pytest.fixture
def owner_auth_token(client, fake_owner_account):
    response = client.post("/api/v1/auth/", json={
        "username": fake_owner_account.username,
        "password": "OwnerPass123!"
    })
    assert response.status_code == 200
    return response.json()["access_token"]
