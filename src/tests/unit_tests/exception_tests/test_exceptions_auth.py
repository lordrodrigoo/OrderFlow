import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
    InvalidCredentialsException,
    AdminForbiddenException,
    token_expired_exception_handler,
    token_invalid_exception_handler,
    invalid_credentials_exception_handler,
    admin_forbidden_exception_handler,
)


@pytest.mark.parametrize("exception, expected_message", [
    (TokenExpiredException(), "Token has expired"),
    (TokenExpiredException("Custom expired msg"), "Custom expired msg"),
    (TokenInvalidException(), "Invalid token"),
    (TokenInvalidException("Custom invalid msg"), "Custom invalid msg"),
    (InvalidCredentialsException(), "Invalid username or password"),
    (InvalidCredentialsException("Custom credentials msg"), "Custom credentials msg"),
    (AdminForbiddenException(), "Admin access required"),
    (AdminForbiddenException("Custom forbidden msg"), "Custom forbidden msg"),
])
def test_exception_attributes(exception, expected_message):
    assert exception.message == expected_message
    assert str(exception) == expected_message


@pytest.mark.asyncio
@pytest.mark.parametrize("exc, handler, expected_status", [
    (TokenExpiredException(), token_expired_exception_handler, status.HTTP_401_UNAUTHORIZED),
    (TokenInvalidException(), token_invalid_exception_handler, status.HTTP_401_UNAUTHORIZED),
    (InvalidCredentialsException(), invalid_credentials_exception_handler, status.HTTP_401_UNAUTHORIZED),
    (AdminForbiddenException(), admin_forbidden_exception_handler, status.HTTP_403_FORBIDDEN),
])
async def test_exception_handlers(exc, handler, expected_status):
    response = await _call_handler(handler, exc)
    assert response.status_code == expected_status
