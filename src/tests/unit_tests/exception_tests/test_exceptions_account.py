# pylint: disable=redefined-outer-name
import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    AccountNotFoundException,
    AccountInactiveException,
    AccountPermissionDeniedException,
    username_exception_handler,
    invalid_credentials_exception_handler,
    account_not_found_exception_handler,
    account_inactive_exception_handler,
    account_permission_denied_exception_handler,
)




@pytest.mark.parametrize("exception, attr, expected_value", [
    (UsernameAlreadyExistsException("testuser"), "username", "testuser"),
    (AccountNotFoundException(42), "account_id", 42),
    (AccountInactiveException(7), "account_id", 7),
    (AccountPermissionDeniedException(99), "account_id", 99),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


def test_invalid_credentials_message():
    exception = InvalidCredentialsException()
    assert "Invalid username or password" in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exc, handler, expected_status", [
    (UsernameAlreadyExistsException("john"),    username_exception_handler,                status.HTTP_409_CONFLICT),
    (InvalidCredentialsException(),             invalid_credentials_exception_handler,     status.HTTP_401_UNAUTHORIZED),
    (AccountNotFoundException(1),               account_not_found_exception_handler,       status.HTTP_404_NOT_FOUND),
    (AccountInactiveException(1),               account_inactive_exception_handler,        status.HTTP_403_FORBIDDEN),
    (AccountPermissionDeniedException(1),       account_permission_denied_exception_handler, status.HTTP_403_FORBIDDEN),
])
async def test_exception_handlers(exc, handler, expected_status):
    response = await _call_handler(handler, exc)
    assert response.status_code == expected_status
