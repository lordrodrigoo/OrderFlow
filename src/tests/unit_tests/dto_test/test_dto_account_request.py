import pytest
from pydantic import ValidationError
from src.dto.request.account_request import (
    AccountRequest,
    UpdateAccountRequest,
    UpdatePasswordRequest
)


def test_valid_account_request():
    account = AccountRequest(user_id=1, username="john_doe", password="P@ssw0rd1")
    assert account.user_id == 1
    assert account.username == "john_doe"
    assert account.password == "P@ssw0rd1"


def test_valid_update_account_request():
    update = UpdateAccountRequest(username="new_user")
    assert update.username == "new_user"


def test_update_account_request_username_none():
    update = UpdateAccountRequest(username=None)
    assert update.username is None


def test_valid_update_password_request():
    req = UpdatePasswordRequest(current_password="OldP@ss1", new_password="NewP@ss1")
    assert req.current_password == "OldP@ss1"
    assert req.new_password == "NewP@ss1"


@pytest.mark.parametrize("field,value,expected_msg", [
    ("user_id", 0, "Input should be greater than 0"),
    ("user_id", -1, "Input should be greater than 0"),
    ("username", "ab", "String should have at least 3 characters"),
    ("username", "a" * 51, "String should have at most 50 characters"),
    ("username", "john@@", "must contain only letters, numbers, dots or underscores."),
    ("password", "short", "String should have at least 8 characters"),
    ("password", "weakpassword", "must contain at least one uppercase, one lowercase and one special character."),
])
def test_account_request_field_validations(field, value, expected_msg):
    valid_data = {"user_id": 1, "username": "john_doe", "password": "P@ssw0rd1"}
    valid_data[field] = value
    with pytest.raises(ValidationError) as exc_info:
        AccountRequest(**valid_data)
    assert expected_msg in str(exc_info.value)


@pytest.mark.parametrize("value,expected_msg", [
    ("ab", "String should have at least 3 characters"),
    ("a" * 51, "String should have at most 50 characters"),
    ("user@@", "must contain only letters, numbers, dots or underscores."),
])
def test_update_account_request_invalid_username(value, expected_msg):
    with pytest.raises(ValidationError) as exc_info:
        UpdateAccountRequest(username=value)
    assert expected_msg in str(exc_info.value)


@pytest.mark.parametrize("field,value,expected_msg", [
    ("current_password", "short", "String should have at least 8 characters"),
    ("new_password", "short", "String should have at least 8 characters"),
    ("new_password", "weakpassword", "must contain at least one uppercase, one lowercase and one special character."),
])
def test_update_password_request_field_validations(field, value, expected_msg):
    valid_data = {"current_password": "OldP@ss1", "new_password": "NewP@ss1"}
    valid_data[field] = value
    with pytest.raises(ValidationError) as exc_info:
        UpdatePasswordRequest(**valid_data)
    assert expected_msg in str(exc_info.value)
