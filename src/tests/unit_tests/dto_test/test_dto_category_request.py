#pylint: disable=redefined-outer-name
import pytest
from pydantic import ValidationError
from src.dto.request.category_request import CategoryRequest


def test_valid_category_request(valid_category_data):
    category_request = CategoryRequest(**valid_category_data)
    assert category_request.name == valid_category_data["name"]
    assert category_request.description == valid_category_data["description"]


@pytest.mark.parametrize("field,value,expected_msg", [
    ("name", None, "Input should be a valid string"),
    ("name", "Pi", "String should have at least 3 characters"),
    ("name", "P" * 21, "String should have at most 20 characters"),
    ("name", "Pizza@123", "must contain only letters, numbers, hyphens or spaces."),
    ("description", None, "Input should be a valid string"),
    ("description", "Short", "String should have at least 10 characters"),
    ("description", "D" * 51, "String should have at most 50 characters"),
])
def test_field_validations(valid_category_data, field, value, expected_msg):
    data = valid_category_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        CategoryRequest(**data)
    assert expected_msg in str(exc_info.value)


def test_invalid_name(valid_category_data):
    # Test invalid name with special characters
    invalid_name = "Pizza@123"
    with pytest.raises(ValidationError) as exc_info:
        CategoryRequest(**{**valid_category_data, "name": invalid_name})
    assert "must contain only letters, numbers, hyphens or spaces." in str(exc_info.value)
