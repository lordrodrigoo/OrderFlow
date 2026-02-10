import pytest
from fastapi.testclient import TestClient
from main import app
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.user import UserEntity
from src.infra.db.entities.account import AccountEntity
from src.domain.models.user import UserRole, Users


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_users():
    sessison = DBConnectionHandler().get_session()
    sessison.query(AccountEntity).delete()
    sessison.query(UserEntity).delete()
    sessison.commit()
    yield
    sessison.close()


@pytest.fixture
def fake_admin_user():
    return  Users(
        first_name="Admin",
        last_name="User",
        age=30,
        email="admin.user@example.com",
        phone="11999999999",
        is_active=True,
        role=UserRole.ADMIN
    )

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
