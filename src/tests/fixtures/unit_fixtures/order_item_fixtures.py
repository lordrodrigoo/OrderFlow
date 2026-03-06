#pylint: disable=redefined-outer-name
from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from src.dto.response.order_item_response import OrderItemResponse
from src.usecases.order_item_usecases import OrderItemUsecase
from src.domain.models.order_item import OrderItem



@pytest.fixture
def order_item_usecase(
    fake_order_item_repository_mock,
    fake_order_repository_mock,
    fake_product_repository_mock
):
    return OrderItemUsecase(
        order_item_repository=fake_order_item_repository_mock,
        order_repository=fake_order_repository_mock,
        product_repository=fake_product_repository_mock
    )


@pytest.fixture
def valid_order_item_data():
    return {
        "order_id": 1,
        "product_id": 1,
        "quantity": 2,
        "unit_price": Decimal("29.90"),
        "subtotal": Decimal("59.80"),
        "notes": "Extra cheese, please"
    }



@pytest.fixture
def fake_order_item_repository_mock():
    repository_mock = MagicMock()
    repository_mock.create_order_item.return_value = OrderItem(
        id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        unit_price=Decimal("29.90"),
        subtotal=Decimal("59.80"),
        notes="Extra cheese, please",
        created_at=datetime.now()
    )
    repository_mock.exists.return_value = False
    return repository_mock


@pytest.fixture
def valid_order_item():
    return OrderItemResponse(
        id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        unit_price=Decimal("29.90"),
        subtotal=Decimal("59.80"),
        notes="Extra cheese, please",
        created_at=datetime.now()
    )
