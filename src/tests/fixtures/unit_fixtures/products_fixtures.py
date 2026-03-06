#pylint: disable=redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.usecases.product_usecases import ProductUsecase
from src.dto.response.product_response import ProductResponse
from src.domain.models.product import Product


@pytest.fixture
def fake_product_response_mock():
    return ProductResponse(
        id=1,
        name="Pizza Margherita",
        description="Deliciosa pizza com molho de tomate, mussarela e manjericão",
        category_id=1,
        price=29.90,
        is_available=True,
        preparation_time=20,
        created_at=datetime.now()
    )

@pytest.fixture
def product_usecase(
    fake_product_repository_mock,
    category_repository_mock
):
    return ProductUsecase(fake_product_repository_mock, category_repository_mock)


@pytest.fixture
def valid_product_data():
    return {
        "name": "Pizza Margherita",
        "description": "Deliciosa pizza com molho de tomate, mussarela e manjericão",
        "category_id": 1,
        "price": 29.90,
        "is_available": True,
        "preparation_time": 20
    }



@pytest.fixture
def fake_product_repository_mock():
    repository_mock = MagicMock()
    repository_mock.get_product_by_id.return_value = None
    repository_mock.find_products_by_name.return_value = None
    repository_mock.create_product.return_value = Product(
        id=1,
        name="Pizza Margherita",
        description="Deliciosa pizza com molho de tomate, mussarela e manjericão",
        category_id=1,
        price=29.90,
        is_available=True,
        preparation_time=20,
        created_at=datetime.now()
    )
    return repository_mock
