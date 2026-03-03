#pylint: disable=unused-argument
import pytest
from pydantic import ValidationError
from src.dto.request.review_request import ReviewRequest
from src.dto.response.review_response import ReviewResponse
from src.exceptions.exception_handlers_review import (
    ReviewNotFoundException,
    InvalidReviewException
)
from src.exceptions.exception_handlers_user import UserNotFoundException
from src.exceptions.exception_handlers_product import ProductNotFoundException


def test_create_review(
        review_usecase,
        fake_review_repository_mock,
        valid_review_data
    ):
    request = ReviewRequest(**valid_review_data)
    response = review_usecase.create_review(request)

    assert isinstance(response, ReviewResponse)
    assert response.user_id == valid_review_data["user_id"]
    assert response.product_id == valid_review_data["product_id"]
    assert response.rating == valid_review_data["rating"]
    assert response.comment == valid_review_data["comment"]


def test_create_review_user_not_found(
        review_usecase,
        fake_user_repository_mock,
        valid_review_request
    ):
    fake_user_repository_mock.find_user_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        review_usecase.create_review(valid_review_request)


def test_create_review_product_not_found(
        review_usecase,
        fake_product_repository_mock_review,
        valid_review_request
    ):
    fake_product_repository_mock_review.find_product_by_id.return_value = None

    with pytest.raises(ProductNotFoundException):
        review_usecase.create_review(valid_review_request)



def test_create_review_with_invalid_data():
    with pytest.raises(ValidationError) as exc_info:
        ReviewRequest(
            user_id=1,
            product_id=1,
            rating=6,  # Invalid rating, should be between 1 and 5
            comment="Great product!"
        )
    assert "Input should be less than or equal to 5" in str(exc_info.value)


def test_get_review_by_id_not_found(
        review_usecase,
        fake_review_repository_mock
    ):
    fake_review_repository_mock.get_review_by_id.return_value = None
    with pytest.raises(ReviewNotFoundException) as exc_info:
        review_usecase.get_review_by_id(999)
    assert "Review with ID: '999' not found." in str(exc_info.value)


def test_list_reviews_invalid_rating_range(
        review_usecase,
    ):
    with pytest.raises(InvalidReviewException):
        review_usecase.list_reviews(min_rating=5, max_rating=1)


def test_list_reviews_user_not_found(
        review_usecase,
        fake_user_repository_mock
    ):
    fake_user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(UserNotFoundException):
        review_usecase.list_reviews(user_id=999)


def test_list_reviews_product_not_found(
        review_usecase,
        fake_product_repository_mock_review
    ):
    fake_product_repository_mock_review.find_product_by_id.return_value = None
    with pytest.raises(ProductNotFoundException):
        review_usecase.list_reviews(product_id=999)


def test_list_reviews_success(
        review_usecase,
        fake_review_repository_mock,
        valid_review
    ):
    fake_review_repository_mock.get_all_reviews.return_value = [valid_review]
    response = review_usecase.list_reviews()
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], ReviewResponse)


def test_get_review_by_id_success(
        review_usecase,
        fake_review_repository_mock,
        valid_review
    ):
    fake_review_repository_mock.get_review_by_id.return_value = valid_review
    response = review_usecase.get_review_by_id(1)
    assert isinstance(response, ReviewResponse)
    assert response.id == valid_review.id
    assert response.user_id == valid_review.user_id
    assert response.product_id == valid_review.product_id
    assert response.rating == valid_review.rating
    assert response.comment == valid_review.comment

def test_delete_review_success(
        review_usecase,
        fake_review_repository_mock,
        valid_review
    ):
    fake_review_repository_mock.get_review_by_id.return_value = valid_review
    review_usecase.delete_review(1)
    fake_review_repository_mock.delete_review.assert_called_once_with(1)


def test_delete_review_not_found(
        review_usecase,
        fake_review_repository_mock
    ):
    fake_review_repository_mock.get_review_by_id.return_value = None
    with pytest.raises(ReviewNotFoundException):
        review_usecase.delete_review(999)
