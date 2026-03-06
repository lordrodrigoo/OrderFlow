import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_category import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
    category_already_exists_exception_handler,
    category_not_found_exception_handler
)


@pytest.mark.parametrize("exception, attr, expected_value", [
    (CategoryNotFoundException(42), "category_id", 42),
    (CategoryAlreadyExistsException("Test Category"), "category_name", "Test Category"),
])
def test_exception_initialization(exception, attr, expected_value):
    assert hasattr(exception, attr)
    assert getattr(exception, attr) == expected_value
    assert str(expected_value) in exception.message


@pytest.mark.asyncio
@pytest.mark.parametrize("exception, handler, expected_status", [
    (CategoryNotFoundException(42),
      category_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (CategoryAlreadyExistsException("Test Category"),
      category_already_exists_exception_handler, status.HTTP_409_CONFLICT),
])
async def test_exception_handlers(exception, handler, expected_status):
    response = await _call_handler(handler, exception)
    assert response.status_code == expected_status
