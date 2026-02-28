#pylint: disable=unused-argument
from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.domain.models.order import OrderStatus, Order
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.exceptions.exception_handlers_order import (
    OrderNotFoundException,
    OrderAlreadyCanceledException
)



def test_create_order(
        order_usecase,
        fake_order_repository_mock,
        valid_order_data
    ):
    request = OrderRequest(**valid_order_data)
    response = order_usecase.create_order(valid_order_data["user_id"], request)

    assert isinstance(response, OrderResponse)
    assert response.user_id == valid_order_data["user_id"]
    assert response.total_amount == Decimal(str(valid_order_data["total_amount"]))
    assert response.delivery_fee == Decimal(str(valid_order_data["delivery_fee"]))
    assert response.notes == valid_order_data["notes"]
    assert response.status.value == "pending"


def test_order_not_found(
        order_usecase,
        fake_order_repository_mock
    ):
    fake_order_repository_mock.get_order_by_id.return_value = None
    with pytest.raises(OrderNotFoundException) as exc_info:
        order_usecase.get_order_by_id(999)
    assert "Order with ID: '999' not found." in exc_info.value.message


def test_create_order_with_invalid_data():
    with pytest.raises(ValidationError) as exc_info:
        OrderRequest(
            user_id=1,
            address_id=1,
            total_amount="invalid_amount",
            delivery_fee="invalid_fee",
            notes="Please deliver between 6-7 PM",
            scheduled_date=datetime.now() + timedelta(days=1)
        )
    assert "Input should be a valid decimal" in str(exc_info.value)



def test_update_order_with_invalid_data(
        order_usecase,
        fake_order_repository_mock,
        valid_order_data,
        valid_order
    ):
    fake_order_repository_mock.get_order_by_id.return_value = valid_order

    invalid_data = valid_order_data.copy()
    invalid_data["total_amount"] = "invalid_amount"
    invalid_data["delivery_fee"] = "invalid_fee"

    with pytest.raises(ValidationError) as exc_info:
        order_usecase.update_order(1, OrderRequest(**invalid_data))
    assert "Input should be a valid decimal" in str(exc_info.value)



def test_order_already_canceled(
        order_usecase,
        fake_order_repository_mock,
        valid_order_data
    ):
    fake_order_repository_mock.get_order_by_id.return_value = Order(
        id=1,
        user_id=valid_order_data["user_id"],
        address_id=valid_order_data["address_id"],
        total_amount=Decimal(str(valid_order_data["total_amount"])),
        delivery_fee=Decimal(str(valid_order_data["delivery_fee"])),
        notes=valid_order_data["notes"],
        scheduled_date=valid_order_data["scheduled_date"],
        status=OrderStatus.CANCELED,
        created_at=datetime.now()
    )
    with pytest.raises(OrderAlreadyCanceledException) as exc_info:
        order_usecase.cancel_order(1)
    assert "Order with ID: '1' is already canceled." in exc_info.value.message


def test_order_invalid_request():
    with pytest.raises(ValidationError) as exc_info:
        OrderRequest(
            user_id=1,
            address_id=1,
            total_amount="invalid_amount",
            delivery_fee="invalid_fee",
            notes="Please deliver between 6-7 PM",
            scheduled_date=datetime.now() + timedelta(days=1)
        )
    assert "Input should be a valid decimal" in str(exc_info.value)


def test_find_all_orders(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_all_orders.return_value = [valid_order]
    response = order_usecase.list_orders()
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], OrderResponse)
    assert response[0].id == valid_order.id
    assert response[0].user_id == valid_order.user_id
    assert response[0].address_id == valid_order.address_id
    assert response[0].total_amount == valid_order.total_amount
    assert response[0].delivery_fee == valid_order.delivery_fee
    assert response[0].notes == valid_order.notes
    assert response[0].scheduled_date == valid_order.scheduled_date
    assert response[0].status == valid_order.status


def test_get_order_by_id(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_order_by_id.return_value = valid_order
    response = order_usecase.get_order_by_id(1)
    assert isinstance(response, OrderResponse)
    assert response.id == valid_order.id
    assert response.user_id == valid_order.user_id
    assert response.address_id == valid_order.address_id
    assert response.total_amount == valid_order.total_amount
    assert response.delivery_fee == valid_order.delivery_fee
    assert response.notes == valid_order.notes
    assert response.scheduled_date == valid_order.scheduled_date
    assert response.status == valid_order.status
