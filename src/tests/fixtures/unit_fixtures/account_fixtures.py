#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.usecases.account_usecases import AccountUsecase
from src.domain.models.account import AccountStatus
from src.domain.models.user import UserRole


@pytest.fixture
def account_repository_mock():
    return MagicMock()


@pytest.fixture
def fake_account():
    class FakeAccount:
        def __init__(self):
            self.id = 1
            self.user_id = 1
            self.username = "john_doe"
            self.password_hash = "hashed_password"
            self.status = AccountStatus.ACTIVE
            self.created_at = datetime.now()
    return FakeAccount()


@pytest.fixture
def fake_user_entity():
    class FakeUser:
        def __init__(self):
            self.id = 1
            self.first_name = "Rodrigo"
            self.last_name = "Souza"
            self.age = 30
            self.email = "rodrigo@example.com"
            self.phone = "11999999999"
            self.is_active = True
            self.role = UserRole.USER
            self.created_at = datetime.now()
    return FakeUser()


@pytest.fixture
def account_usecase(account_repository_mock, user_repository_mock):
    return AccountUsecase(account_repository_mock, user_repository_mock)
