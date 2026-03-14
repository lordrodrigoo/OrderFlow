#pylint: disable=unused-argument
from datetime import timedelta
import pytest
from jose import jwt
from src.config.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
)
from src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
)


# ──────────────────────────────────────────────
# hash_password / verify_password
# ──────────────────────────────────────────────

def test_hash_password_returns_string():
    hashed = hash_password("mysecretpassword")
    assert isinstance(hashed, str)
    assert hashed != "mysecretpassword"


def test_verify_password_correct():
    hashed = hash_password("correctpassword")
    assert verify_password("correctpassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("correctpassword")
    assert verify_password("wrongpassword", hashed) is False


# ──────────────────────────────────────────────
# create_access_token
# ──────────────────────────────────────────────

def test_create_access_token_returns_string():
    token = create_access_token({"sub": "user@example.com", "user_id": 1})
    assert isinstance(token, str)


def test_create_access_token_payload():
    token = create_access_token({"sub": "user@example.com", "user_id": 1})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user@example.com"
    assert payload["user_id"] == 1


def test_create_access_token_custom_expiry():
    token = create_access_token(
        {"sub": "user@example.com", "user_id": 1},
        expires_delta=timedelta(minutes=5)
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


# ──────────────────────────────────────────────
# create_refresh_token
# ──────────────────────────────────────────────

def test_create_refresh_token_returns_string():
    token = create_refresh_token({"sub": "user@example.com", "user_id": 1})
    assert isinstance(token, str)


def test_create_refresh_token_payload():
    token = create_refresh_token({"sub": "user@example.com", "user_id": 1})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user@example.com"
    assert payload["user_id"] == 1


def test_create_refresh_token_custom_expiry():
    token = create_refresh_token(
        {"sub": "user@example.com", "user_id": 1},
        expires_delta=timedelta(days=1)
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


# ──────────────────────────────────────────────
# verify_token
# ──────────────────────────────────────────────

def test_verify_token_valid():
    token = create_access_token({"sub": "user@example.com", "user_id": 1})
    payload = verify_token(token)
    assert payload.sub == "user@example.com"
    assert payload.user_id == 1


def test_verify_token_expired():
    token = create_access_token(
        {"sub": "user@example.com", "user_id": 1},
        expires_delta=timedelta(seconds=-1)
    )
    with pytest.raises(TokenExpiredException):
        verify_token(token)


def test_verify_token_invalid():
    with pytest.raises(TokenInvalidException):
        verify_token("this.is.not.a.valid.token")
