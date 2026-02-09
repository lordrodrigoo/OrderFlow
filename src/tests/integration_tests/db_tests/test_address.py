#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from src.infra.db.entities.address import AddressEntity


def test_create_address(db_session, fake_user, fake_address):
    assert fake_address.id is not None
    assert fake_address.street == "Main St"
    assert fake_address.user_id == fake_user.id


def test_update_address(db_session, fake_user, fake_address):
    fake_address.street = "Plaza St"
    db_session.commit()
    updated_address = db_session.query(AddressEntity).filter_by(id=fake_address.id).first()
    assert updated_address.street == "Plaza St"


def test_search_address_by_street(db_session, fake_user, fake_address):
    searched_address = db_session.query(AddressEntity).filter_by(street="Main St").first()
    assert searched_address is not None
    assert searched_address.id == fake_address.id


def test_search_all_addresses(db_session, fake_user, fake_address):
    addresses = db_session.query(AddressEntity).all()
    assert len(addresses) >= 1


def test_search_address_by_id(db_session, fake_user, fake_address):
    found_address = db_session.query(AddressEntity).filter_by(id=fake_address.id).first()
    assert found_address is not None
    assert found_address.street == fake_address.street


def test_relationship_between_user_and_address(db_session, fake_user, fake_address):
    addres = db_session.query(AddressEntity).filter_by(id=fake_address.id).first()
    assert addres.user.id == fake_user.id
    assert addres.user.email == fake_user.email


def test_delete_address(db_session, fake_user, fake_address):
    db_session.delete(fake_address)
    db_session.commit()
    delete_address = db_session.query(AddressEntity).filter_by(id=fake_address.id).first()
    assert delete_address is None
