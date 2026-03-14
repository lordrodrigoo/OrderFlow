#pylint: disable=redefined-outer-name
from decimal import Decimal
from datetime import timedelta, datetime
import pytest
from pydantic import ValidationError
from src.dto.request.order_request import OrderRequest


def test_valid_order_request(valid_order_data):
    order_request = OrderRequest(**valid_order_data)
    assert order_request.address_id == valid_order_data["address_id"]
    assert order_request.total_amount == Decimal(str(valid_order_data["total_amount"]))
    assert order_request.delivery_fee == Decimal(str(valid_order_data["delivery_fee"]))
    assert order_request.notes == valid_order_data["notes"]
    assert order_request.scheduled_date == valid_order_data["scheduled_date"]


@pytest.mark.parametrize("field,value,expected_msg", [
    ("address_id", None, "Input should be a valid integer"),
    ("address_id", "abc", "Input should be a valid integer"),
    ("address_id", 0, "Input should be greater than 0"),
    ("address_id", -1, "Input should be greater than 0"),
    ("scheduled_date", datetime.now() - timedelta(days=1), "Scheduled date must be in the future"),
    ("scheduled_date", datetime.now() + timedelta(days=31), "Scheduled date cannot be more than 30 days in the future"),
    ("scheduled_date", "invalid", "Input should be a valid datetime"),
    ("scheduled_date", "2026-01-01", "Scheduled date must be in the future"),
    ("notes", 123, "Input should be a valid string"),
    ("notes", "a" * 256, "String should have at most 255 characters"),
    ("total_amount", None, "Decimal input should be an integer, float, string or Decimal object"),
    ("total_amount", -1, "Input should be greater than 0"),
    ("total_amount", 100000.01, "Input should be less than or equal to 10000"),
    ("total_amount", 9.999, "Decimal input should have no more than 2 decimal places"),
    ("total_amount", "invalid", "Input should be a valid decimal"),
    ("delivery_fee", None, "Decimal input should be an integer, float, string or Decimal object"),
    ("delivery_fee", -1, "Input should be greater than or equal to 0"),
    ("delivery_fee", 100000.01, "Input should be less than or equal to 10000"),
    ("delivery_fee", 9.999, "Decimal input should have no more than 2 decimal places"),
    ("delivery_fee", "invalid", "Input should be a valid decimal"),
])
def test_field_validations(valid_order_data, field, value, expected_msg):
    data = valid_order_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        OrderRequest(**data)
    assert expected_msg in str(exc_info.value)


def test_invalid_scheduled_date(valid_order_data):
    # Test scheduled_date in the past
    past_date = valid_order_data["scheduled_date"] - timedelta(days=1)
    with pytest.raises(ValidationError) as exc_info:
        OrderRequest(**{**valid_order_data, "scheduled_date": past_date})
    assert "Scheduled date must be in the future" in str(exc_info.value)


def test_order_request_notes_strip(valid_order_data):
    data = valid_order_data.copy()
    data["notes"] = "  My note  "
    req = OrderRequest(**data)
    assert req.notes == "My note"


def test_order_request_notes_none(valid_order_data):
    data = valid_order_data.copy()
    data["notes"] = None
    req = OrderRequest(**data)
    assert req.notes is None


def test_order_request_notes_empty_string(valid_order_data):
    data = valid_order_data.copy()
    data["notes"] = "   "
    with pytest.raises(ValidationError) as exc_info:
        OrderRequest(**data)
    assert "Notes cannot be empty string" in str(exc_info.value)
