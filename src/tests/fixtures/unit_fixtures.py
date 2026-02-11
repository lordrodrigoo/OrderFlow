#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from passlib.context import CryptContext
from src.usecases.user_usecases import UserUsecase
from src.usecases.auth_user_usecases import AuthUserUsecase
from src.dto.request.user_request import CreateUserRequest
from src.dto.request.address_request import AddressRequest
from src.usecases.address_usecase import AddressUsecase
from src.dto.response.address_response import AddressResponse

@pytest.fixture
def user_repository_mock():
    repo = MagicMock()
    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.first_name = "Rodrigo"
    user_mock.last_name = "Souza"
    user_mock.age = 30
    user_mock.phone = "11999999999"
    user_mock.email = "rodrigo.souza@example.com"
    user_mock.is_active = True
    user_mock.role = "user"
    user_mock.created_at = datetime.now()
    repo.create_user.return_value = user_mock

    return repo

@pytest.fixture
def user_response_mock():
    return MagicMock(
        id=1,
        first_name="Rodrigo",
        last_name="Souza",
        age=30,
        phone="11999999999",
        email="rodrigo.souza@example.com",
        role="user",
        is_active=True,
        created_at=datetime.now()
    )


@pytest.fixture
def account_repository_mock():
    return MagicMock()

@pytest.fixture
def usecase(user_repository_mock, account_repository_mock):
    return UserUsecase(user_repository_mock, account_repository_mock)


@pytest.fixture
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture
def usecase_auth(user_repository_mock, account_repository_mock, pwd_context):
    return AuthUserUsecase(user_repository_mock, account_repository_mock, pwd_context)


@pytest.fixture
def account_mock():
    account = MagicMock()
    account.user_id = 1
    account.password_hash = "$2b$12$KIXQJHj8e5Z5u1s9z1e7Oe5u1s9z1e7Oe5u1s9z1e7Oe5u1s9z1e7Oe5u"
    return account


@pytest.fixture
def make_valid_request():
    return CreateUserRequest(
        first_name="John",
        last_name="Lennon",
        email="john.lennon@example.com",
        phone="1191234-5678",
        password="StrongPass@123",
        role="user"
    )


@pytest.fixture
def address_usecase(fake_address_repository_mock):
    return AddressUsecase(fake_address_repository_mock)


@pytest.fixture
def valid_address_data():
    return {
        "user_id": 1,
        "street": "rua Ipiranga",
        "number": "456",
        "neighborhood": "Centro",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "03433023",
        "is_default": True,
        "complement": "casa 2 fundos"
    }


@pytest.fixture
def valid_address_request(valid_address_data):
    return AddressRequest(**valid_address_data)


@pytest.fixture
def fake_address_response_mock():
    return AddressResponse(
        id=1,
        user_id=1,
        street="rua Ipiranga",
        number="456",
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="03433023",
        is_default=True,
        complement="casa 2 fundos",
        created_at=datetime.now()
    )


@pytest.fixture
def fake_address_repository_mock():
    repository_mock = MagicMock()
    repository_mock.create_address.return_value = MagicMock(
        id=1,
        user_id=1,
        street="rua Ipiranga",
        number="456",
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="03433023",
        is_default=True,
        complement="casa 2 fundos",
        created_at=datetime.now()
    )
    repository_mock.find_address_by_id.return_value = None
    return repository_mock
