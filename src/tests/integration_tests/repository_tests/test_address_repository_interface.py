from src.domain.models.address import Address
from src.infra.db.repositories.address_repository_interface import AddressRepository
from src.tests.helpers import FakeDBConnectionHandler


def test_update_address(fake_address, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    address_repo = AddressRepository(db_handler)

    address = Address.from_entity(fake_address)
    address.street = "Updated Street"
    address.number = "456"
    address.neighborhood = "Vila Nova Gonçalves"
    address.complement = "Casa"
    address.city = "Rio de Janeiro"
    address.state = "RJ"
    address.zip_code = "03433000"
    address.is_default = False


    updated_address = address_repo.update_address(address)
    assert updated_address.street == "Updated Street"
    assert updated_address.number == "456"
    assert updated_address.neighborhood == "Vila Nova Gonçalves"
    assert updated_address.complement == "Casa"
    assert updated_address.city == "Rio de Janeiro"
    assert updated_address.state == "RJ"
    assert updated_address.zip_code == "03433000"
    assert updated_address.is_default is False


def test_find_by_zip_code(fake_address, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    address_repo = AddressRepository(db_handler)

    found_addresses = address_repo.find_by_zip_code(fake_address.zip_code)
    assert isinstance(found_addresses, list)
    assert any(address.id == fake_address.id for address in found_addresses)



def test_set_default_address_returns_none_when_address_does_not_belong_to_user(fake_address, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    address_repo = AddressRepository(db_handler)

    wrong_user_id = fake_address.user_id + 999

    result = address_repo.set_default_address(fake_address.id, wrong_user_id)

    assert result is None
