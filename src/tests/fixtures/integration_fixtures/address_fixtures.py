# pylint:disable=unused-argument
from datetime import datetime
import pytest
from src.infra.db.entities.address import AddressEntity


@pytest.fixture
def fake_address(db_session, fake_user):
    address = AddressEntity(
        user_id=fake_user.id,
        street="Main St",
        number="123",
        complement="Apt 4",
        neighborhood="Downtown",
        city="Metropolis",
        state="NY",
        zip_code="12345",
        is_default=True,
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(address)
    db_session.commit()
    return address


@pytest.fixture
def valid_address_data(fake_user):
    return {
        "user_id": fake_user.id,
        "street": "Ipiranga Avenue",
        "number": "123",
        "complement": "Apt 4",
        "neighborhood": "Vila Mariana",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "03433000",
        "is_default": True
    }
