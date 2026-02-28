#pylint: disable=redefined-outer-name
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from src.dto.request.order_request import OrderRequest
from src.usecases.order_usecases import OrderUsecase
from src.dto.response.order_response import OrderResponse
from src.domain.models.order import Order, OrderStatus


@pytest.fixture
def fake_order_response_mock():
    return OrderResponse(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("59.90"),
        delivery_fee=Decimal("5.00"),
        notes="Please deliver between 6-7 PM",
        scheduled_date=datetime(2026, 6, 30, 18),
        status=OrderStatus.PENDING,
        created_at=datetime.now()
    )



@pytest.fixture
def order_usecase(
    fake_order_repository_mock
):
    return OrderUsecase(fake_order_repository_mock)



@pytest.fixture
def valid_order_data():
    return {
        "user_id": 1,
        "address_id": 1,
        "total_amount": Decimal("59.90"),
        "delivery_fee": Decimal("5.00"),
        "notes": "Please deliver between 6-7 PM",
        "scheduled_date": datetime.now() + timedelta(days=1)
    }


@pytest.fixture
def valid_order_request(valid_order_data):
    return OrderRequest(**valid_order_data)



@pytest.fixture
def fake_order_repository_mock():
    repository_mock = MagicMock()
    repository_mock.get_order_by_id.return_value = None
    repository_mock.create_order.return_value = Order(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("59.90"),
        delivery_fee=Decimal("5.00"),
        notes="Please deliver between 6-7 PM",
        scheduled_date=datetime.now() + timedelta(days=1),
        status=OrderStatus.PENDING,
        created_at=datetime.now()
    )
    return repository_mock


@pytest.fixture
def valid_order():
    return Order(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("59.90"),
        delivery_fee=Decimal("5.00"),
        notes="Please deliver between 6-7 PM",
        scheduled_date=datetime.now() + timedelta(days=1),
        status=OrderStatus.PENDING,
        created_at=datetime.now()
    )
