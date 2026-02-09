import pytest
from pydantic import ValidationError
from src.dto.request.auth_user_request import AuthUserRequest

def test_valid_auth_user_request():
    req = AuthUserRequest(username="user123", password="Password@123")
    assert req.username == "user123"
    assert req.password == "Password@123"


def test_invalid_username_too_short():
    with pytest.raises(ValidationError):
        AuthUserRequest(username="ab", password="Password@123")


def test_invalid_username_non_alphanumeric():
    with pytest.raises(ValidationError):
        AuthUserRequest(username="user!@#", password="Password@123")


def test_invalid_password_too_short():
    with pytest.raises(ValidationError):
        AuthUserRequest(username="user123", password="abc")


def test_invalid_password_no_uppercase_or_special():
    with pytest.raises(ValidationError):
        AuthUserRequest(username="user123", password="password1234")


def test_invalid_password_no_special():
    with pytest.raises(ValidationError):
        AuthUserRequest(username="user123", password="Password1234")
