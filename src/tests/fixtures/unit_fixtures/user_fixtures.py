#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.usecases.user_usecases import UserUsecase




@pytest.fixture
def user_repository_mock():
    repo = MagicMock()
    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.first_name = "Rodrigo"
    user_mock.last_name = "Souza"
    user_mock.age = 30
    user_mock.phone = "11999999999"
    user_mock.email = "rodrigo.souza@example.com"
    user_mock.is_active = True
    user_mock.role = "user"
    user_mock.created_at = datetime.now()
    repo.create_user.return_value = user_mock

    return repo


@pytest.fixture
def usecase(user_repository_mock, account_repository_mock):
    return UserUsecase(user_repository_mock, account_repository_mock)
