#pylint: disable=redefined-outer-name
import pytest
from pydantic import ValidationError
from src.dto.request.user_request import CreateUserRequest
from src.domain.models.user import UserRole



def test_valid_user_request(valid_user_data):
    user_request = CreateUserRequest(**valid_user_data)
    assert user_request.first_name == valid_user_data["first_name"]
    assert user_request.last_name == valid_user_data["last_name"]
    assert user_request.age == valid_user_data["age"]
    assert user_request.email == valid_user_data["email"]
    assert user_request.phone == valid_user_data["phone"]
    assert user_request.username == valid_user_data["username"]
    assert user_request.password == valid_user_data["password"]
    assert user_request.role == UserRole.USER


@pytest.mark.parametrize("field,value,expected_msg", [
        ("first_name", "Ro", "String should have at least 3 characters"),
        ("first_name", "R" * 26, "String should have at most 25 characters"),
        ("first_name", "John123", "must contain only letters."),
        ("last_name", "So", "String should have at least 3 characters"),
        ("last_name", "S" * 26, "String should have at most 25 characters"),
        ("last_name", "Doe123", "must contain only letters."),
        ("age", 15, "Input should be greater than or equal to 16"),
        ("age", 121, "age must be less than or equal to 120 years old."),
        ("email", "invalid-email", "value is not a valid email address"),
        ("phone", "123456789", "String should have at least 10 characters"),
        ("phone", "1" * 16, "String should have at most 15 characters"),
        ("phone", "12345abcde", "phone must contain only numeric characters."),
        ("username", "ro", "String should have at least 3 characters"),
        ("username", "r" * 51, "String should have at most 50 characters"),
        ("username", "john@@", "username must contain only letters, numbers, dots or underscores."),
        ("password", "short", "String should have at least 8 characters"),
        ("password", "weakpassword", "password must contain at least one uppercase"),
])
def test_field_validations(valid_user_data, field, value, expected_msg):
    data = valid_user_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert expected_msg in str(exc_info.value)
