#pylint: disable=unused-argument
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.domain.models.order import OrderStatus, Order
from src.dto.request.order_item_request import OrderItemRequest
from src.dto.response.order_item_response import OrderItemResponse
from src.exceptions.exception_handlers_order_item import (
    OrderItemNotFoundException,
    InvalidOrderItemException,
    DuplicateOrderItemException
)
from src.exceptions.exception_handlers_order import OrderNotFoundException

def test_create_order_item(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data
    ):
    request = OrderItemRequest(**valid_order_item_data)
    response = order_item_usecase.create_order_item(request)

    assert isinstance(response, OrderItemResponse)
    assert response.order_id == valid_order_item_data["order_id"]
    assert response.product_id == valid_order_item_data["product_id"]
    assert response.quantity == valid_order_item_data["quantity"]
    assert response.unit_price == Decimal(str(valid_order_item_data["unit_price"]))
    assert response.notes == valid_order_item_data["notes"]


def test_order_item_not_found(
        order_item_usecase,
        fake_order_item_repository_mock
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = None
    with pytest.raises(OrderItemNotFoundException) as exc_info:
        order_item_usecase.get_order_item_by_id(999)
    assert "Order item with ID: '999' not found." in str(exc_info.value)



def test_create_order_item_with_invalid_data():
    with pytest.raises(ValidationError) as exc_info:
        OrderItemRequest(
            order_id=1,
            product_id=1,
            quantity="invalid_quantity",
            unit_price="invalid_price",
            notes="Extra spicy"
        )
    assert "Input should be a valid integer" in str(exc_info.value)
    assert "Input should be a valid decimal" in str(exc_info.value)


def test_update_order_item_with_invalid_data(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    with pytest.raises(ValidationError) as exc_info:
        OrderItemRequest(
            order_id=valid_order_item_data["order_id"],
            product_id=valid_order_item_data["product_id"],
            quantity="invalid_quantity",
            unit_price="invalid_price",
            notes="Extra spicy"
        )
    assert "Input should be a valid integer" in str(exc_info.value)
    assert "Input should be a valid decimal" in str(exc_info.value)


def test_update_order_item(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item
    fake_order_item_repository_mock.update_order_item.return_value = valid_order_item

    updated_data = valid_order_item_data.copy()
    updated_data["quantity"] = 3
    updated_data["unit_price"] = Decimal("19.99")

    response = order_item_usecase.update_order_item(1, OrderItemRequest(**updated_data))

    assert isinstance(response, OrderItemResponse)
    assert response.order_id == updated_data["order_id"]
    assert response.product_id == updated_data["product_id"]
    assert response.quantity == updated_data["quantity"]
    assert response.unit_price == Decimal(str(updated_data["unit_price"]))
    assert response.notes == updated_data["notes"]


def test_duplicate_order_item(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item
    fake_order_item_repository_mock.exists.return_value = True
    with pytest.raises(DuplicateOrderItemException) as exc_info:
        order_item_usecase.create_order_item(OrderItemRequest(**valid_order_item_data))
    assert "Product '1' is already associated with order '1'." in str(exc_info.value)



def test_invalid_order_item_status(
        order_item_usecase,
        fake_order_repository_mock,
        valid_order_item_data
    ):
    fake_order_repository_mock.get_order_by_id.return_value = Order(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("100.00"),
        delivery_fee=Decimal("5.00"),
        notes="Please deliver between 6-7 PM",
        status=OrderStatus.CANCELED
    )
    with pytest.raises(InvalidOrderItemException) as exc_info:
        order_item_usecase.create_order_item(OrderItemRequest(**valid_order_item_data))
    assert "Cannot add items to order ID: '1' with status: 'canceled'." in str(exc_info.value)



def test_deleted_order_item(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = None
    with pytest.raises(OrderItemNotFoundException) as exc_info:
        order_item_usecase.get_order_item_by_id(1)
    assert "Order item with ID: '1' not found." in str(exc_info.value)


def test_find_all_order_items_by_order_id(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_items_by_order_id.return_value = [valid_order_item]
    order_item_usecase.order_repository.exists.return_value = True

    response = order_item_usecase.list_order_items(order_id=1)

    assert isinstance(response, list)
    assert len(response) == 1
    assert isinstance(response[0], OrderItemResponse)
    assert response[0].order_id == valid_order_item_data["order_id"]
    assert response[0].product_id == valid_order_item_data["product_id"]
    assert response[0].quantity == valid_order_item_data["quantity"]
    assert response[0].unit_price == Decimal(str(valid_order_item_data["unit_price"]))
    assert response[0].notes == valid_order_item_data["notes"]


def test_get_order_item_by_id(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item

    response = order_item_usecase.get_order_item_by_id(1)

    assert isinstance(response, OrderItemResponse)
    assert response.order_id == valid_order_item_data["order_id"]
    assert response.product_id == valid_order_item_data["product_id"]
    assert response.quantity == valid_order_item_data["quantity"]
    assert response.unit_price == Decimal(str(valid_order_item_data["unit_price"]))


def test_subtotal_calculation(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item

    response = order_item_usecase.get_order_item_by_id(1)

    expected_subtotal = Decimal(str(valid_order_item_data["quantity"])) * Decimal(str(valid_order_item_data["unit_price"]))
    assert response.subtotal == expected_subtotal
    assert response.order_id == valid_order_item_data["order_id"]
    assert response.product_id == valid_order_item_data["product_id"]
    assert response.quantity == valid_order_item_data["quantity"]
    assert response.unit_price == Decimal(str(valid_order_item_data["unit_price"]))
    assert response.notes == valid_order_item_data["notes"]


def test_delete_order_item_not_found(
        order_item_usecase,
        fake_order_item_repository_mock
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = None
    with pytest.raises(OrderItemNotFoundException) as exc_info:
        order_item_usecase.delete_order_item(999)
    assert "Order item with ID: '999' not found." in str(exc_info.value)


def test_delete_order_item_invalid_status(
        order_item_usecase,
        fake_order_item_repository_mock,
        fake_order_repository_mock,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item
    fake_order_repository_mock.get_order_by_id.return_value = Order(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("100.00"),
        delivery_fee=Decimal("5.00"),
        status=OrderStatus.DELIVERED
    )
    with pytest.raises(InvalidOrderItemException):
        order_item_usecase.delete_order_item(1)


def test_update_order_item_not_found(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item_data
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = None
    with pytest.raises(OrderItemNotFoundException) as exc_info:
        order_item_usecase.update_order_item(999, OrderItemRequest(**valid_order_item_data))
    assert "Order item with ID: '999' not found." in str(exc_info.value)


def test_update_order_item_invalid_status(
        order_item_usecase,
        fake_order_item_repository_mock,
        fake_order_repository_mock,
        valid_order_item_data,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_order_item_by_id.return_value = valid_order_item
    fake_order_repository_mock.get_order_by_id.return_value = Order(
        id=1,
        user_id=1,
        address_id=1,
        total_amount=Decimal("100.00"),
        delivery_fee=Decimal("5.00"),
        status=OrderStatus.CANCELED
    )
    with pytest.raises(InvalidOrderItemException):
        order_item_usecase.update_order_item(1, OrderItemRequest(**valid_order_item_data))


def test_list_order_items_all(
        order_item_usecase,
        fake_order_item_repository_mock,
        valid_order_item
    ):
    fake_order_item_repository_mock.get_all_order_items.return_value = [valid_order_item]
    response = order_item_usecase.list_order_items()
    assert isinstance(response, list)
    assert len(response) == 1


def test_list_order_items_order_not_found(
        order_item_usecase,
        fake_order_repository_mock
    ):
    fake_order_repository_mock.exists.return_value = False
    with pytest.raises(OrderNotFoundException):
        order_item_usecase.list_order_items(order_id=999)
