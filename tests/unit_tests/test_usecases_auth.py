from unittest.mock import MagicMock
import pytest
from src.dto.request.auth_user_request import AuthUserRequest
from src.dto.response.auth_user_response import AuthUserResponse
from src.exceptions.exception_handlers import InvalidCredentialsException

def test_authenticate_success(
        usecase_auth,
        account_mock,
        user_repository_mock,
        account_repository_mock
    ):

    account_repository_mock.find_by_username.return_value = account_mock
    user_repository_mock.find_user_by_id.return_value = MagicMock(id=1)

    # Mock pwd_context.verify to return True
    usecase_auth.pwd_context.verify = lambda pw, h: True
    request = AuthUserRequest(username="usuario123", password="Senha@123")
    response = usecase_auth.authenticate_user(request)

    assert isinstance(response, AuthUserResponse)
    assert response.access_token
    assert response.token_type == "bearer"


def test_authenticate_invalid_username(usecase_auth, account_repository_mock):
    account_repository_mock.find_by_username.return_value = None
    request = AuthUserRequest(username="usuario123", password="Senha@123")
    with pytest.raises(InvalidCredentialsException):
        usecase_auth.authenticate_user(request)

def test_authenticate_invalid_password(
        usecase_auth, account_mock,
        user_repository_mock,
        account_repository_mock
    ):

    account_repository_mock.find_by_username.return_value = account_mock
    user_repository_mock.find_user_by_id.return_value = MagicMock(id=1)

    # Mock pwd_context.verify to return False
    usecase_auth.pwd_context.verify = lambda pw, h: False
    request = AuthUserRequest(username="usuario123", password="Senha@123")
    with pytest.raises(InvalidCredentialsException):
        usecase_auth.authenticate_user(request)
