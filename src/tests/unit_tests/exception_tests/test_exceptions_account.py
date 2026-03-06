# pylint: disable=redefined-outer-name
import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    username_exception_handler,
    invalid_credentials_exception_handler
)




@pytest.mark.parametrize("exception, attr, expected_value", [
    (UsernameAlreadyExistsException("testuser"), "username", "testuser")
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


def test_invalid_credentials_message():
    exception = InvalidCredentialsException()
    assert "Invalid username or password" in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exc, handler, expected_status", [
    (UsernameAlreadyExistsException("john"), username_exception_handler,             status.HTTP_409_CONFLICT),
    (InvalidCredentialsException(),          invalid_credentials_exception_handler,  status.HTTP_401_UNAUTHORIZED),
])
async def test_exception_handlers(exc, handler, expected_status):
    response = await _call_handler(handler, exc)
    assert response.status_code == expected_status
