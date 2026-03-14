#pylint: disable=unused-argument
from unittest.mock import MagicMock, patch
import pytest
from src.domain.models.account import AccountStatus
from src.dto.request.account_request import AccountRequest, UpdateAccountRequest, UpdatePasswordRequest
from src.dto.request.login_request import LoginRequest
from src.dto.response.account_response import AccountResponse
from src.dto.response.token_response import TokenResponse
from src.dto.response.user_response import UserResponse
from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    AccountInactiveException,
    AccountNotFoundException,
    AccountPermissionDeniedException,
)


# ──────────── create_account ────────────

@patch("src.usecases.account_usecases.hash_password", return_value="hashed_pw")
def test_create_account_success(mock_hash, account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_by_username.return_value = None
    account_repository_mock.create_account.return_value = fake_account
    response = account_usecase.create_account(AccountRequest(user_id=1, username="john_doe", password="P@ssw0rd1"))
    assert isinstance(response, AccountResponse)
    assert response.username == "john_doe"


def test_create_account_username_exists(account_usecase, account_repository_mock):
    account_repository_mock.find_by_username.return_value = MagicMock()
    with pytest.raises(UsernameAlreadyExistsException):
        account_usecase.create_account(AccountRequest(user_id=1, username="john_doe", password="P@ssw0rd1"))


# ──────────── login ────────────

@patch("src.usecases.account_usecases.create_access_token", return_value="tok123")
@patch("src.usecases.account_usecases.verify_password", return_value=True)
def test_login_success(mock_verify, mock_token, account_usecase, account_repository_mock, user_repository_mock, fake_account):
    account_repository_mock.find_by_username.return_value = fake_account
    user_repository_mock.find_user_by_id.return_value = MagicMock()
    result = account_usecase.login(LoginRequest(username="john_doe", password="P@ssw0rd1"))
    assert isinstance(result, TokenResponse)
    assert result.access_token == "tok123"


@patch("src.usecases.account_usecases.verify_password", return_value=False)
def test_login_account_not_found(mock_verify, account_usecase, account_repository_mock):
    account_repository_mock.find_by_username.return_value = None
    with pytest.raises(InvalidCredentialsException):
        account_usecase.login(LoginRequest(username="unknown", password="P@ssw0rd1"))


def test_login_account_inactive(account_usecase, account_repository_mock, fake_account):
    fake_account.status = AccountStatus.INACTIVE
    account_repository_mock.find_by_username.return_value = fake_account
    with pytest.raises(AccountInactiveException):
        account_usecase.login(LoginRequest(username="john_doe", password="P@ssw0rd1"))


@patch("src.usecases.account_usecases.verify_password", return_value=False)
def test_login_wrong_password(mock_verify, account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_by_username.return_value = fake_account
    with pytest.raises(InvalidCredentialsException):
        account_usecase.login(LoginRequest(username="john_doe", password="WrongP@ss1"))


@patch("src.usecases.account_usecases.verify_password", return_value=True)
def test_login_user_not_found(mock_verify, account_usecase, account_repository_mock, user_repository_mock, fake_account):
    account_repository_mock.find_by_username.return_value = fake_account
    user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(InvalidCredentialsException):
        account_usecase.login(LoginRequest(username="john_doe", password="P@ssw0rd1"))


# ──────────── get_authenticated_user ────────────

def test_get_authenticated_user_success(account_usecase, user_repository_mock, fake_user_entity):
    user_repository_mock.find_by_email.return_value = fake_user_entity
    response = account_usecase.get_authenticated_user("rodrigo@example.com")
    assert isinstance(response, UserResponse)


def test_get_authenticated_user_not_found(account_usecase, user_repository_mock):
    user_repository_mock.find_by_email.return_value = None
    with pytest.raises(InvalidCredentialsException):
        account_usecase.get_authenticated_user("notfound@example.com")


# ──────────── get_account_by_id ────────────

def test_get_account_by_id_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    response = account_usecase.get_account_by_id(1)
    assert isinstance(response, AccountResponse)
    assert response.username == "john_doe"


def test_get_account_by_id_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.get_account_by_id(999)


# ──────────── update_account ────────────

def test_update_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.find_by_username.return_value = None
    account_repository_mock.update_account.return_value = fake_account
    response = account_usecase.update_account(1, UpdateAccountRequest(username="new_name"), current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_update_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.update_account(999, UpdateAccountRequest(username="new_name"), current_user_id=1)


def test_update_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.update_account(1, UpdateAccountRequest(username="new_name"), current_user_id=999)


def test_update_account_username_exists(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.find_by_username.return_value = MagicMock()
    with pytest.raises(UsernameAlreadyExistsException):
        account_usecase.update_account(1, UpdateAccountRequest(username="existing"), current_user_id=1)


# ──────────── update_password ────────────

@patch("src.usecases.account_usecases.hash_password", return_value="new_hashed")
@patch("src.usecases.account_usecases.verify_password", return_value=True)
def test_update_password_success(mock_verify, mock_hash, account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.update_password.return_value = fake_account
    response = account_usecase.update_password(
        1,
        UpdatePasswordRequest(current_password="OldP@ss1", new_password="NewP@ss1"),
        current_user_id=1
    )
    assert isinstance(response, AccountResponse)


def test_update_password_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.update_password(
            999,
            UpdatePasswordRequest(current_password="OldP@ss1", new_password="NewP@ss1"),
            current_user_id=1
        )


def test_update_password_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.update_password(
            1,
            UpdatePasswordRequest(current_password="OldP@ss1", new_password="NewP@ss1"),
            current_user_id=999
        )


@patch("src.usecases.account_usecases.verify_password", return_value=False)
def test_update_password_wrong_current(mock_verify, account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(InvalidCredentialsException):
        account_usecase.update_password(
            1,
            UpdatePasswordRequest(current_password="WrongP@ss1", new_password="NewP@ss1"),
            current_user_id=1
        )


# ──────────── deactivate_account ────────────

def test_deactivate_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.update_status.return_value = fake_account
    response = account_usecase.deactivate_account(1, current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_deactivate_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.deactivate_account(999, current_user_id=1)


def test_deactivate_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.deactivate_account(1, current_user_id=999)


# ──────────── suspend_account ────────────

def test_suspend_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.update_status.return_value = fake_account
    response = account_usecase.suspend_account(1, current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_suspend_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.suspend_account(999, current_user_id=1)


def test_suspend_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.suspend_account(1, current_user_id=999)


# ──────────── inactivate_account ────────────

def test_inactivate_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.update_status.return_value = fake_account
    response = account_usecase.inactivate_account(1, current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_inactivate_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.inactivate_account(999, current_user_id=1)


def test_inactivate_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.inactivate_account(1, current_user_id=999)


# ──────────── activate_account ────────────

def test_activate_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    account_repository_mock.update_status.return_value = fake_account
    response = account_usecase.activate_account(1, current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_activate_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.activate_account(999, current_user_id=1)


def test_activate_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.activate_account(1, current_user_id=999)


# ──────────── delete_account ────────────

def test_delete_account_success(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    response = account_usecase.delete_account(1, current_user_id=1)
    assert isinstance(response, AccountResponse)


def test_delete_account_not_found(account_usecase, account_repository_mock):
    account_repository_mock.find_account_by_id.return_value = None
    with pytest.raises(AccountNotFoundException):
        account_usecase.delete_account(999, current_user_id=1)


def test_delete_account_permission_denied(account_usecase, account_repository_mock, fake_account):
    account_repository_mock.find_account_by_id.return_value = fake_account
    with pytest.raises(AccountPermissionDeniedException):
        account_usecase.delete_account(1, current_user_id=999)
