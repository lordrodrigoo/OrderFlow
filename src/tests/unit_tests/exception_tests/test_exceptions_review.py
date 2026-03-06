import pytest
from fastapi import status
from src.tests.helpers import _call_handler
from src.exceptions.exception_handlers_review import (
    ReviewNotFoundException,
    InvalidReviewException,
    review_not_found_exception_handler,
    invalid_review_exception_handler,
)


@pytest.mark.parametrize("exception, expected_value", [
    (ReviewNotFoundException(99), "99"),
    (ReviewNotFoundException(99, user_id=1), "user_id=1"),
    (ReviewNotFoundException(99, product_id=2), "product_id=2"),
    (ReviewNotFoundException(99, user_id=1, product_id=5), "user_id=1"),
])
def test_exception_attributes(exception, expected_value):
    assert expected_value in exception.message



@pytest.mark.asyncio
@pytest.mark.parametrize("exc, handler, expected_status", [
    (ReviewNotFoundException(99),
     review_not_found_exception_handler, status.HTTP_404_NOT_FOUND),

    (InvalidReviewException("Rating must be between 1 and 5."),
     invalid_review_exception_handler, status.HTTP_400_BAD_REQUEST),
])
async def test_exception_handlers(exc, handler, expected_status):
    response = await _call_handler(handler, exc)
    assert response.status_code == expected_status
