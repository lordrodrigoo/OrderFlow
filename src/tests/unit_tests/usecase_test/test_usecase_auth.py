#pylint: disable=unused-argument
from unittest.mock import MagicMock, patch
import pytest
from src.dto.response.token_response import TokenResponse
from src.domain.models.account import AccountStatus
from src.exceptions.exception_handlers_account import (
    InvalidCredentialsException,
    AccountInactiveException
)


@patch("src.usecases.auth_usecases.create_refresh_token", return_value="refresh_tok")
@patch("src.usecases.auth_usecases.create_access_token", return_value="access_tok")
@patch("src.usecases.auth_usecases.verify_password", return_value=True)
def test_login_success(mock_verify, mock_access, mock_refresh, auth_usecase, auth_account_repo, auth_user_repo, active_account, fake_auth_user):
    auth_account_repo.find_by_username.return_value = active_account
    auth_user_repo.find_user_by_id.return_value = fake_auth_user

    result = auth_usecase.login("rodrigo", "P@ssw0rd1")

    assert isinstance(result, TokenResponse)
    assert result.access_token == "access_tok"
    assert result.refresh_token == "refresh_tok"
    assert result.token_type == "bearer"


@patch("src.usecases.auth_usecases.verify_password", return_value=False)
def test_login_account_not_found(mock_verify, auth_usecase, auth_account_repo):
    auth_account_repo.find_by_username.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("unknown", "P@ssw0rd1")


def test_login_account_inactive(auth_usecase, auth_account_repo, active_account):
    active_account.status = AccountStatus.INACTIVE
    auth_account_repo.find_by_username.return_value = active_account

    with pytest.raises(AccountInactiveException):
        auth_usecase.login("rodrigo", "P@ssw0rd1")


@patch("src.usecases.auth_usecases.verify_password", return_value=False)
def test_login_wrong_password(mock_verify, auth_usecase, auth_account_repo, active_account):
    auth_account_repo.find_by_username.return_value = active_account

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("rodrigo", "WrongPass1!")


@patch("src.usecases.auth_usecases.verify_password", return_value=True)
def test_login_user_not_found(mock_verify, auth_usecase, auth_account_repo, auth_user_repo, active_account):
    auth_account_repo.find_by_username.return_value = active_account
    auth_user_repo.find_user_by_id.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("rodrigo", "P@ssw0rd1")


@patch("src.usecases.auth_usecases.create_access_token", return_value="new_access_tok")
@patch("src.usecases.auth_usecases.verify_token")
def test_refresh_token_success(mock_verify_token, mock_access, auth_usecase, auth_account_repo, auth_user_repo, active_account, fake_auth_user):
    payload = MagicMock()
    payload.user_id = 1
    mock_verify_token.return_value = payload
    auth_user_repo.find_user_by_id.return_value = fake_auth_user
    auth_account_repo.find_by_user_id.return_value = active_account

    result = auth_usecase.refresh_token("valid_refresh_token")

    assert isinstance(result, TokenResponse)
    assert result.access_token == "new_access_tok"
    assert result.refresh_token == "valid_refresh_token"


@patch("src.usecases.auth_usecases.verify_token")
def test_refresh_token_user_not_found(mock_verify_token, auth_usecase, auth_user_repo):
    payload = MagicMock()
    payload.user_id = 99
    mock_verify_token.return_value = payload
    auth_user_repo.find_user_by_id.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.refresh_token("some_token")


@patch("src.usecases.auth_usecases.verify_token")
def test_refresh_token_account_not_found(mock_verify_token, auth_usecase, auth_account_repo, auth_user_repo, fake_auth_user):
    payload = MagicMock()
    payload.user_id = 1
    mock_verify_token.return_value = payload
    auth_user_repo.find_user_by_id.return_value = fake_auth_user
    auth_account_repo.find_by_user_id.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.refresh_token("some_token")


@patch("src.usecases.auth_usecases.verify_token")
def test_refresh_token_account_inactive(mock_verify_token, auth_usecase, auth_account_repo, auth_user_repo, active_account, fake_auth_user):
    payload = MagicMock()
    payload.user_id = 1
    mock_verify_token.return_value = payload
    auth_user_repo.find_user_by_id.return_value = fake_auth_user
    active_account.status = AccountStatus.INACTIVE
    auth_account_repo.find_by_user_id.return_value = active_account

    with pytest.raises(AccountInactiveException):
        auth_usecase.refresh_token("some_token")
