#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.usecases.review_usecases import ReviewUsecase
from src.dto.request.review_request import ReviewRequest
from src.domain.models.review import Review


@pytest.fixture
def fake_user_repository_mock():
    repository_mock = MagicMock()
    repository_mock.find_user_by_id.return_value = MagicMock(id=1)
    return repository_mock


@pytest.fixture
def fake_product_repository_mock_review():
    repository_mock = MagicMock()
    repository_mock.find_product_by_id.return_value = MagicMock(id=1)
    return repository_mock


@pytest.fixture
def review_usecase(
    fake_review_repository_mock,
    fake_user_repository_mock,
    fake_product_repository_mock_review
):
    return ReviewUsecase(
        review_repository=fake_review_repository_mock,
        user_repository=fake_user_repository_mock,
        product_repository=fake_product_repository_mock_review
    )


@pytest.fixture
def valid_review_data():
    return {
        "user_id": 1,
        "product_id": 1,
        "rating": 5,
        "comment": "Great product!"
    }

@pytest.fixture
def valid_review_request(valid_review_data):
    return ReviewRequest(**valid_review_data)


@pytest.fixture
def fake_review_repository_mock():
    repository_mock = MagicMock()
    repository_mock.create_review.return_value = Review(
        id=1,
        user_id=1,
        product_id=1,
        rating=5,
        comment="Great product!",
        created_at=datetime.now()
    )
    return repository_mock


@pytest.fixture
def valid_review():
    return Review(
        id=1,
        user_id=1,
        product_id=1,
        rating=5,
        comment="Great product!",
        created_at=datetime.now()
    )
