import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_address import (
    AddressNotFoundException,
    AddressPermissionDeniedException,
    AddressAlreadyExistsException,
    address_not_found_exception_handler,
    address_permission_denied_exception_handler,
    address_already_exists_exception_handler
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (AddressNotFoundException(42), "address_id", 42),
    (AddressAlreadyExistsException("123 Main St"), "address", "123 Main St"),
    (AddressPermissionDeniedException(99), "address_id", 99),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


def test_address_permission_denied_message():
    exception = AddressPermissionDeniedException(99)
    assert "permission" in exception.message
    assert "address with ID: '99'" in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exception, handler, expected_status", [
    (AddressNotFoundException(42),
      address_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (AddressAlreadyExistsException("123 Main St"),
      address_already_exists_exception_handler, status.HTTP_409_CONFLICT),

    (AddressPermissionDeniedException(99),
      address_permission_denied_exception_handler, status.HTTP_403_FORBIDDEN),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
