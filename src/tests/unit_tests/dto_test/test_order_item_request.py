#pylint: disable=redefined-outer-name
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.dto.request.order_item_request import OrderItemRequest




def test_valid_order_item_request(valid_order_item_data):
    order_item_request = OrderItemRequest(**valid_order_item_data)
    assert order_item_request.order_id == valid_order_item_data["order_id"]
    assert order_item_request.product_id == valid_order_item_data["product_id"]
    assert order_item_request.quantity == valid_order_item_data["quantity"]
    assert order_item_request.unit_price == Decimal(str(valid_order_item_data["unit_price"]))
    assert order_item_request.notes == valid_order_item_data["notes"]


@pytest.mark.parametrize("field,value,expected_msg", [
    ("order_id", None, "Input should be a valid integer"),
    ("order_id", "abc", "Input should be a valid integer"),
    ("order_id", 0, "Input should be greater than 0"),
    ("order_id", -1, "Input should be greater than 0"),
    ("product_id", None, "Input should be a valid integer"),
    ("product_id", "abc", "Input should be a valid integer"),
    ("product_id", 0, "Input should be greater than 0"),
    ("product_id", -1, "Input should be greater than 0"),
    ("quantity", None, "Input should be a valid integer"),
    ("quantity", "abc", "Input should be a valid integer"),
    ("quantity", 0, "Input should be greater than 0"),
    ("quantity", -1, "Input should be greater than 0"),
    ("unit_price", None, "Decimal input should be an integer, float, string or Decimal object"),
    ("unit_price", -1, "Input should be greater than 0"),
    ("unit_price", 100000.01, "Input should be less than or equal to 10000"),
    ("unit_price", 9.999, "Decimal input should have no more than 2 decimal places"),
    ("unit_price", "invalid", "Input should be a valid decimal"),
    ("notes", 123, "Input should be a valid string"),
    ("notes", "a" * 256, "String should have at most 255 characters"),
])
def test_field_validations(valid_order_item_data, field, value, expected_msg):
    data = valid_order_item_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        OrderItemRequest(**data)
    assert expected_msg in str(exc_info.value)


def test_order_item_request_notes_strip():
    req = OrderItemRequest(order_id=1, product_id=1, quantity=1, unit_price=10.0, notes="  some note  ")
    assert req.notes == "some note"


def test_order_item_request_notes_none():
    req = OrderItemRequest(order_id=1, product_id=1, quantity=1, unit_price=10.0, notes=None)
    assert req.notes is None


def test_order_item_request_notes_empty_string():
    with pytest.raises(ValidationError) as exc_info:
        OrderItemRequest(order_id=1, product_id=1, quantity=1, unit_price=10.0, notes="   ")
    assert "Notes cannot be empty string" in str(exc_info.value)
