#pylint: disable=unused-argument
from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.domain.models.order import OrderStatus, Order
from src.dto.request.order_request import OrderRequest
from src.dto.response.order_response import OrderResponse
from src.dto.response.dashboard_response import DashboardResponse
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
    response = order_usecase.create_order(request, valid_order_data["user_id"])

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
        order_usecase.get_order_by_id(999, 1)
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
        order_usecase.cancel_order(1, 1)
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
    response = order_usecase.get_order_by_id(1, 1)
    assert isinstance(response, OrderResponse)
    assert response.id == valid_order.id
    assert response.user_id == valid_order.user_id
    assert response.address_id == valid_order.address_id
    assert response.total_amount == valid_order.total_amount
    assert response.delivery_fee == valid_order.delivery_fee
    assert response.notes == valid_order.notes
    assert response.scheduled_date == valid_order.scheduled_date
    assert response.status == valid_order.status


def test_cancel_order_not_found(
        order_usecase,
        fake_order_repository_mock
    ):
    fake_order_repository_mock.get_order_by_id.return_value = None
    with pytest.raises(OrderNotFoundException) as exc_info:
        order_usecase.cancel_order(999, 1)
    assert "Order with ID: '999' not found." in exc_info.value.message


def test_list_orders_filter_by_amount(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_all_orders.return_value = [valid_order]
    response = order_usecase.list_orders(
        min_amount=Decimal("50.00"),
        max_amount=Decimal("100.00")
    )
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], OrderResponse)
    assert response[0].id == valid_order.id


def test_list_orders_filter_by_amount_no_match(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_all_orders.return_value = [valid_order]
    response = order_usecase.list_orders(
        min_amount=Decimal("500.00"),
        max_amount=Decimal("1000.00")
    )
    assert response == []


def test_admin_update_order_status(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_order_by_id.return_value = valid_order
    response = order_usecase.admin_update_order_status(1, OrderStatus.PAID)
    assert isinstance(response, OrderResponse)
    assert response.status == OrderStatus.PAID


def test_admin_update_order_status_not_found(
        order_usecase,
        fake_order_repository_mock
    ):
    fake_order_repository_mock.get_order_by_id.return_value = None
    with pytest.raises(OrderNotFoundException):
        order_usecase.admin_update_order_status(999, OrderStatus.PAID)


def test_admin_get_all_orders(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_all_orders.return_value = [valid_order]
    response = order_usecase.admin_get_all_orders()
    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], OrderResponse)


def test_admin_get_all_orders_filter_by_status(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.find_orders_by_status.return_value = [valid_order]
    response = order_usecase.admin_get_all_orders(order_status="pending")
    assert len(response) == 1
    fake_order_repository_mock.find_orders_by_status.assert_called_once_with("pending")


def test_admin_get_all_orders_filter_by_user(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.find_orders_by_user.return_value = [valid_order]
    response = order_usecase.admin_get_all_orders(user_id=1)
    assert len(response) == 1
    fake_order_repository_mock.find_orders_by_user.assert_called_once_with(1)


def test_get_dashboard_stats(
        order_usecase,
        fake_order_repository_mock,
        valid_order
    ):
    fake_order_repository_mock.get_all_orders.return_value = [valid_order]
    response = order_usecase.get_dashboard_stats(total_users=5, total_products=10)
    assert isinstance(response, DashboardResponse)
    assert response.total_orders == 1
    assert response.total_users == 5
    assert response.total_products == 10
    assert response.total_revenue >= 0
    assert isinstance(response.orders_by_status, dict)


def test_get_dashboard_stats_excludes_canceled_revenue(
        order_usecase,
        fake_order_repository_mock
    ):
    canceled_order = Order(
        id=2, user_id=1, address_id=1,
        total_amount=Decimal("100.00"), delivery_fee=Decimal("5.00"),
        status=OrderStatus.CANCELED, created_at=datetime.now()
    )
    fake_order_repository_mock.get_all_orders.return_value = [canceled_order]
    response = order_usecase.get_dashboard_stats(total_users=1, total_products=1)
    assert response.total_revenue == 0.0
