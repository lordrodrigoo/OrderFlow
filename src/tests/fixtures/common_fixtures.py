#pylint: disable=redefined-outer-name
import pytest
from sqlalchemy import text
from fastapi.testclient import TestClient
from src.main import app
from src.infra.db.settings.connection import DBConnectionHandler
from src.domain.models.user import UserRole, Users


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_users():
    session = DBConnectionHandler().get_session()
    session.execute(text("DELETE FROM addresses"))
    session.execute(text("DELETE FROM accounts"))
    session.execute(text("DELETE FROM users"))
    session.execute(text("ALTER SEQUENCE addresses_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE accounts_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1"))
    session.commit()
    yield
    session.close()


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

@pytest.fixture
def created_user(client, valid_user_data):
    response = client.post("/api/v1/users/", json=valid_user_data)
    return response.json()["id"]



@pytest.fixture
def valid_address_data(created_user):
    return {
        "user_id": created_user,
        "street": "Rua Exemplo",
        "number": "123A",
        "complement": "Apto 45",
        "neighborhood": "Bairro Exemplo",
        "city": "Cidade Exemplo",
        "state": "SP",
        "zip_code": "12345-678"
    }
