#pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.domain.models.account import AccountStatus
from src.usecases.auth_usecases import AuthUseCases


@pytest.fixture
def auth_account_repo():
    return MagicMock()


@pytest.fixture
def auth_user_repo():
    return MagicMock()


@pytest.fixture
def auth_usecase(auth_account_repo, auth_user_repo):
    return AuthUseCases(auth_account_repo, auth_user_repo)


@pytest.fixture
def active_account():
    account = MagicMock()
    account.id = 1
    account.user_id = 1
    account.status = AccountStatus.ACTIVE
    account.password_hash = "hashed_password"
    return account


@pytest.fixture
def fake_auth_user():
    user = MagicMock()
    user.id = 1
    user.email = "rodrigo@example.com"
    user.role = MagicMock()
    user.role.value = "user"
    return user
