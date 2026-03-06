#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.usecases.address_usecase import AddressUsecase
from src.dto.response.address_response import AddressResponse



@pytest.fixture
def fake_address_response_mock():
    return AddressResponse(
        id=1,
        user_id=1,
        street="Rua Exemplo",
        number="123",
        neighborhood="Centro",
        city="São Paulo",
        state="SP",
        zip_code="12345-678",
        is_default=True,
        complement="casa 2 fundos",
        created_at=datetime.now()
    )


@pytest.fixture
def address_usecase(fake_address_repository_mock):
    return AddressUsecase(fake_address_repository_mock)


@pytest.fixture
def valid_address_data():
    return {
        "user_id": 1,
        "street": "Rua Exemplo",
        "number": "123",
        "neighborhood": "Centro",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "12345-678",
        "is_default": True,
        "complement": "casa 2 fundos"
    }



@pytest.fixture
def fake_address_repository_mock():
    repository_mock = MagicMock()
    repository_mock.find_addresses_by_user_street_number.return_value = None
    repository_mock.create_address.return_value = MagicMock(
        id=1,
        user_id=1,
        street="Rua Exemplo",
        number="123A",
        neighborhood="Bairro Exemplo",
        city="Cidade Exemplo",
        state="SP",
        zip_code="12345-678",
        is_default=True,
        complement="Apto 45",
        created_at=datetime.now()
    )
    repository_mock.find_address_by_id.return_value = None
    return repository_mock
