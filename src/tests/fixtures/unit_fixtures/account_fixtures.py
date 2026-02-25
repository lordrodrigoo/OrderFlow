#pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from passlib.context import CryptContext



@pytest.fixture
def account_repository_mock():
    return MagicMock()


@pytest.fixture
def pwd_context():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")



@pytest.fixture
def account_mock():
    account = MagicMock()
    account.user_id = 1
    account.password_hash = "$2b$12$KIXQJHj8e5Z5u1s9z1e7Oe5u1s9z1e7Oe5u1s9z1e7Oe5u1s9z1e7Oe5u"
    return account
