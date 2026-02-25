#pylint: disable=redefined-outer-name
from decimal import Decimal
import pytest
from pydantic import ValidationError
from src.dto.request.product_request import ProductRequest



def test_valid_product_request(valid_product_data):
    product_request = ProductRequest(**valid_product_data)
    assert product_request.name == valid_product_data["name"]
    assert product_request.description == valid_product_data["description"]
    assert product_request.category_id == valid_product_data["category_id"]
    assert product_request.price == Decimal(str(valid_product_data["price"]))
    assert product_request.is_available == valid_product_data["is_available"]
    assert product_request.preparation_time == valid_product_data["preparation_time"]


@pytest.mark.parametrize("field,value,expected_msg", [
    ("category_id", None, "Input should be a valid integer"),
    ("category_id", "abc", "Input should be a valid integer"),
    ("category_id", 0, "Input should be greater than or equal to 1"),
    ("category_id", -1, "Input should be greater than or equal to 1"),
    ("name", None, "Input should be a valid string"),
    ("name", "Pi", "String should have at least 3 characters"),
    ("name", "P" * 101, "String should have at most 100 characters"),
    ("name", "Pizza@123", "must contain only letters, numbers, hyphens or spaces."),
    ("description", None, "Input should be a valid string"),
    ("description", "Short", "String should have at least 10 characters"),
    ("description", "D" * 501, "String should have at most 500 characters"),
    ("price", None, "Decimal input should be an integer, float, string or Decimal object"),
    ("price", -1, "Input should be greater than or equal to 0"),
    ("price", 10000.01, "Input should be less than or equal to 10000"),
    ("price", 9.999, "Decimal input should have no more than 2 decimal places"),
    ("price", "dez", "Input should be a valid decimal"),
    ("is_available", "OK", "Input should be a valid boolean"),
    ("is_available", None, "Input should be a valid boolean"),
    ("preparation_time", None, "Input should be a valid integer"),
    ("preparation_time", 0, "Input should be greater than or equal to 1"),
    ("preparation_time", -5, "Input should be greater than or equal to 1"),
])
def test_field_validations(valid_product_data, field, value, expected_msg):
    data = valid_product_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        ProductRequest(**data)
    assert expected_msg in str(exc_info.value)


def test_invalid_name(valid_product_data):
    # Test invalid name with special characters
    invalid_name = "Pizza@123"
    with pytest.raises(ValidationError) as exc_info:
        ProductRequest(**{**valid_product_data, "name": invalid_name})
    assert "must contain only letters, numbers, hyphens or spaces." in str(exc_info.value)
