#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.dto.request.category_request import CategoryRequest
from src.usecases.category_usecases import CategoryUsecase
from src.dto.response.category_response import CategoryResponse
from src.domain.models.category import Category




@pytest.fixture
def fake_category_response_mock():
    return CategoryResponse(
        id=1,
        name="Pizzas",
        description="Categoria de pizzas deliciosas",
        created_at=datetime.now()
    )


@pytest.fixture
def category_usecase(
    category_repository_mock
):
    return CategoryUsecase(category_repository_mock)


@pytest.fixture
def valid_category_data():
    return {
        "name": "Pizzas",
        "description": "Categoria de pizzas deliciosas"
    }



@pytest.fixture
def category_repository_mock():
    repository_mock = MagicMock()
    repository_mock.find_by_name.return_value = None
    repository_mock.create_category.return_value = Category(
        id=1,
        name="Pizzas",
        description="Categoria de pizzas deliciosas"
    )
    return repository_mock


@pytest.fixture
def valid_category_request(valid_category_data):
    return CategoryRequest(**valid_category_data)
