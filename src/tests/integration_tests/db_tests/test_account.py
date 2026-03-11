#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
import pytest
from src.infra.db.entities.account import AccountEntity


def test_create_account(db_session, fake_user, fake_account):
    assert fake_account.id is not None
    assert fake_account.username == "ana_silva"
    assert fake_account.user_id == fake_user.id


def test_update_account(db_session, fake_account):
    fake_account.username = "ana_souza"
    db_session.commit()
    updated_account = db_session.query(AccountEntity).filter_by(id=fake_account.id).first()
    assert updated_account.username == "ana_souza"


def test_relationship_between_user_and_account(db_session, fake_user, fake_account):
    # This test I will use fake_account to access the user relationship
    account = db_session.query(AccountEntity).filter_by(id=fake_account.id).first()
    assert account.user.id == fake_account.user_id
    assert account.user.email == fake_account.user.email


def test_account_username_is_unique(db_session, fake_account):
    """This test checks if the username field in AccountEntity is unique.
    I'm using fake_user to create a duplicate account with the same username.
    """
    another_account = AccountEntity(
        user_id=2,
        username=fake_account.username,  # Duplicate username
        password_hash="hash2",
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(another_account)
    with pytest.raises(Exception):
        db_session.commit()


def test_delete_account(db_session, fake_account):
    db_session.delete(fake_account)
    db_session.commit()

    deleted_account = db_session.query(AccountEntity).filter_by(id=fake_account.id).first()
    assert deleted_account is None
