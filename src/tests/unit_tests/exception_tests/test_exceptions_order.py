import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_order import (
    OrderNotFoundException,
    OrderAlreadyCanceledException,
    order_already_canceled_exception_handler,
    order_not_found_exception_handler,
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (OrderNotFoundException(42), "order_id", 42),
    (OrderAlreadyCanceledException(42), "order_id", 42),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exception, handler, expected_status", [
    (OrderNotFoundException(42),
     order_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (OrderAlreadyCanceledException(42),
     order_already_canceled_exception_handler, status.HTTP_409_CONFLICT),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
