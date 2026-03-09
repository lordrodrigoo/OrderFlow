import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductCategoryNotFoundException,
    InvalidPriceProductException,
    product_already_exists_exception_handler,
    product_not_found_exception_handler,
    product_category_not_found_exception_handler,
    invalid_price_product_exception_handler
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (ProductNotFoundException(42), "product_id", 42),
    (ProductAlreadyExistsException("Test Product"), "product_name", "Test Product"),
    (ProductCategoryNotFoundException(99), "category_id", 99),
    (InvalidPriceProductException(), "message", "Price must be greater than zero."),
])
def test_exception_attributes(exception, attr, expected_value):
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exception, handler, expected_status", [
    (ProductNotFoundException(42),
      product_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (ProductAlreadyExistsException("Test Product"),
      product_already_exists_exception_handler, status.HTTP_409_CONFLICT),

    (ProductCategoryNotFoundException(99),
      product_category_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (InvalidPriceProductException(),
      invalid_price_product_exception_handler, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
