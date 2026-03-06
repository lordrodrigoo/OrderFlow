import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_order_item import (
    OrderItemNotFoundException,
    InvalidOrderItemException,
    DuplicateOrderItemException,
    order_item_not_found_exception_handler,
    invalid_order_item_exception_handler,
    duplicate_order_item_exception_handler,
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (OrderItemNotFoundException(order_item_id=1), "order_item_id", 1),
    (InvalidOrderItemException(order_id=1, status="canceled"), "order_id", 1),
    (InvalidOrderItemException(order_id=1, status="canceled"), "status", "canceled"),
    (DuplicateOrderItemException(order_id=1, product_id=2), "order_id", 1),
    (DuplicateOrderItemException(order_id=1, product_id=2), "product_id", 2),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


@pytest.mark.parametrize("exception, handler, expected_status", [
    (OrderItemNotFoundException(order_item_id=1),
     order_item_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (InvalidOrderItemException(order_id=1, status="canceled"),
     invalid_order_item_exception_handler, status.HTTP_400_BAD_REQUEST),

    (DuplicateOrderItemException(order_id=1, product_id=2),
     duplicate_order_item_exception_handler, status.HTTP_400_BAD_REQUEST),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
