import pytest
from src.domain.models.account import Account, AccountStatus
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.tests.helpers import FakeDBConnectionHandler



def test_update_account(fake_account, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)

    account = Account.from_entity(fake_account)
    account.username = "ana_silva_updated"
    account.password_hash = "NewStrongHashedPassword456!"
    account.status = AccountStatus.INACTIVE

    updated_account = account_repo.update_account(account)
    assert updated_account.username == "ana_silva_updated"
    assert updated_account.password_hash == "NewStrongHashedPassword456!"
    assert updated_account.status == AccountStatus.INACTIVE


def test_update_account_without_id(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)
    account = Account(username="no_id", password_hash="hash", status=AccountStatus.ACTIVE, user_id=1)
    with pytest.raises(ValueError):
        account_repo.update_account(account)


def test_update_account_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)
    account = Account(id=9999, username="not_found", password_hash="hash", status=AccountStatus.ACTIVE, user_id=1)
    result = account_repo.update_account(account)
    assert result is None


def test_find_all_accounts(fake_account, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)

    accounts = account_repo.find_all_accounts()
    assert isinstance(accounts, list)
    assert any(account.id == fake_account.id for account in accounts)


def test_find_account_by_id(fake_account, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)

    found_account = account_repo.find_account_by_id(fake_account.id)
    assert found_account is not None
    assert found_account.id == fake_account.id
    assert found_account.username == fake_account.username
    assert found_account.password_hash == fake_account.password_hash
    assert found_account.status == AccountStatus(fake_account.status)


def test_delete_account(fake_account, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    account_repo = AccountRepository(db_handler)

    result = account_repo.delete_account(fake_account.id)
    assert result is True
    assert account_repo.find_account_by_id(fake_account.id) is None
