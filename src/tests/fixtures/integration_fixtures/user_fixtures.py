from datetime import datetime
import pytest
from src.infra.db.entities.user import UserEntity


@pytest.fixture
def user_login_data(fake_account):
    return {
        "username": fake_account.username,
        "password": "StrongPassword123!"
    }

@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Rodrigo",
        "last_name": "Souza",
        "age": 30,
        "email": "rodrigo.souza@example.com",
        "phone": "11999999999",
        "password": "@1234StrongPass",
        "username": "rodrigo.souza",
        "role": "user"
    }



@pytest.fixture
def fake_user(db_session):
    user = UserEntity(
        first_name="Ana",
        last_name="Silva",
        age=28,
        email="ana.silva@example.com",
        phone="123456789",
        is_active=True,
        role="user",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(user)
    db_session.commit()
    return user
