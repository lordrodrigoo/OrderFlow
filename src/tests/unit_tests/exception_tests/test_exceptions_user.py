import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException,
    UserNotFoundException,
    UserPermissionDeniedException,
    email_exception_handler,
    user_not_found_exception_handler,
    user_permission_denied_exception_handler
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (EmailAlreadyExistsException("test@email.com"), "email", "test@email.com"),
    (UserNotFoundException(99), "user_id", 99),
    (UserPermissionDeniedException(1), "user_id", 1),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


def test_user_permission_denied_message():
    exception = UserPermissionDeniedException(1)
    assert "permission" in exception.message
    assert "user with ID: '1'" in exception.message



@pytest.mark.asyncio
@pytest.mark.parametrize("exception, handler, expected_status", [

    (EmailAlreadyExistsException("test@email.com"),
      email_exception_handler, status.HTTP_409_CONFLICT),

    (UserNotFoundException(99),
      user_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (UserPermissionDeniedException(1),
      user_permission_denied_exception_handler, status.HTTP_403_FORBIDDEN),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
