#pylint: disable=redefined-outer-name
import pytest
from pydantic import ValidationError
from src.dto.request.user_request import CreateUserRequest


@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Rodrigo",
        "last_name": "Souza",
        "age": 30,
        "email": "rodrigo.souza@example.com",
        "phone": "11999999999",
        "password": "@1234StrongPass",
        "username": "rodrigo.souza"
    }

def assert_field_error_msg(exc_info, field, expected_msg):
    errors = exc_info.value.errors()
    assert any(error['loc'] == (field,) and expected_msg in error['msg'] for error in errors)


def test_first_name_short_and_long(valid_user_data):
    data = valid_user_data.copy()
    data["first_name"] = "Ro"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "first_name",
        "String should have at least 3 characters")

    data["first_name"] = "R" * 51
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "first_name",
        "String should have at most 25 characters"
    )


def test_last_name_short_and_long(valid_user_data):
    data = valid_user_data.copy()
    data["last_name"] = "So"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "last_name",
        "String should have at least 3 characters"
    )

    data["last_name"] = "S" * 51
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "last_name",
        "String should have at most 25 characters"
    )

def test_age_bellow_minimum(valid_user_data):
    data = valid_user_data.copy()
    data["age"] = 15
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "age",
        "Input should be greater than or equal to 16"
    )


def test_invalid_email_format(valid_user_data):
    data = valid_user_data.copy()
    data["email"] = "invalid-email"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "email",
        "value is not a valid email address"
    )


def test_phone_short_and_long(valid_user_data):
    data = valid_user_data.copy()
    data["phone"] = "123456789"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "phone",
        "String should have at least 10 characters"
    )

    data["phone"] = "1" * 16
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "phone",
        "String should have at most 15 characters"
    )


def test_phone_non_numeric(valid_user_data):
    data = valid_user_data.copy()
    data["phone"] = "12345abcde"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    print(exc_info.value)
    assert_field_error_msg(
        exc_info,
        "phone",
        "must contain only numeric characters"
    )


def test_username_short_and_long(valid_user_data):
    data = valid_user_data.copy()
    data["username"] = "ro"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "username",
        "String should have at least 3 characters"
    )

    data["username"] = "r" * 51
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "username",
        "String should have at most 50 characters"
    )


def test_short_password(valid_user_data):
    data = valid_user_data.copy()
    data["password"] = "short"
    with pytest.raises(ValidationError) as exc_info:
        CreateUserRequest(**data)
    assert_field_error_msg(
        exc_info,
        "password",
        "String should have at least 8 characters"
    )


def test_valid_user_request(valid_user_data):
    user_request = CreateUserRequest(**valid_user_data)
    assert user_request.first_name == valid_user_data["first_name"]
    assert user_request.last_name == valid_user_data["last_name"]
    assert user_request.age == valid_user_data["age"]
    assert user_request.email == valid_user_data["email"]
    assert user_request.phone == valid_user_data["phone"]
    assert user_request.username == valid_user_data["username"]
    assert user_request.password == valid_user_data["password"]
