import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
    InvalidCredentialsException,
    token_expired_exception_handler,
    token_invalid_exception_handler,
    invalid_credentials_exception_handler,
)


@pytest.mark.parametrize("exception, expected_message", [
    (TokenExpiredException(), "Token has expired"),
    (TokenExpiredException("Custom expired msg"), "Custom expired msg"),
    (TokenInvalidException(), "Invalid token"),
    (TokenInvalidException("Custom invalid msg"), "Custom invalid msg"),
    (InvalidCredentialsException(), "Invalid username or password"),
    (InvalidCredentialsException("Custom credentials msg"), "Custom credentials msg"),
])
def test_exception_attributes(exception, expected_message):
    assert exception.message == expected_message
    assert str(exception) == expected_message


@pytest.mark.asyncio
@pytest.mark.parametrize("exc, handler", [
    (TokenExpiredException(), token_expired_exception_handler),
    (TokenInvalidException(), token_invalid_exception_handler),
    (InvalidCredentialsException(), invalid_credentials_exception_handler),
])
async def test_exception_handlers(exc, handler):
    response = await _call_handler(handler, exc)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
