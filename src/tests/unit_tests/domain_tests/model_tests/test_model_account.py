from src.domain.models.account import Account, AccountStatus


def test_create_account():
    account = Account.create_account(
        user_id=1,
        username="testuser",
        password_hash="hashedpassword",
        status= AccountStatus.ACTIVE
    )
    assert account.user_id == 1
    assert account.username == "testuser"
    assert account.password_hash == "hashedpassword"
    assert account.status == AccountStatus.ACTIVE


def test_is_active_property():
    active_account = Account.create_account(
        user_id=1,
        username="activeuser",
        password_hash="hashedpassword",
        status=AccountStatus.ACTIVE
    )
    inactive_account = Account.create_account(
        user_id=2,
        username="inactiveuser",
        password_hash="hashedpassword",
        status=AccountStatus.INACTIVE
    )
    assert active_account.is_active is True
    assert inactive_account.is_active is False
