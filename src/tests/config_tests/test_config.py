#pylint: disable=unused-argument
from datetime import timedelta
from unittest.mock import patch, MagicMock
import pytest
from jose import jwt
from src.config.owner import seed_owner
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


# ──────────────────────────────────────────────
# seed_owner
# ──────────────────────────────────────────────

def test_seed_owner_skipped_when_env_vars_missing():
    """Seeder must do nothing when OWNER_* vars are absent (test environment)."""

    with patch.dict("os.environ", {}, clear=False):
        with patch("src.config.owner.os.getenv", side_effect=lambda k, *a: None):
            with patch("src.config.owner.DBConnectionHandler") as mock_db:
                seed_owner()
                mock_db.assert_not_called()


def test_seed_owner_skipped_when_owner_already_exists():
    """Seeder must not create a second owner if one already exists."""

    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "owner",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_role.return_value = [MagicMock()]

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)
        mock_db_instance.session = MagicMock()

        with patch("src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("src.config.owner.UserRepository", return_value=mock_user_repo):
                with patch("src.config.owner.AccountRepository"):
                    seed_owner()
                    mock_user_repo.create_user.assert_not_called()


def test_seed_owner_creates_owner_when_none_exists():
    """Seeder creates owner user and account when no owner exists yet."""

    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "owner",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_role.return_value = []
        mock_user_repo.find_by_email.return_value = None
        created_user = MagicMock()
        created_user.id = 1
        mock_user_repo.create_user.return_value = created_user

        mock_acc_repo = MagicMock()
        mock_acc_repo.find_by_username.return_value = None

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)
        mock_db_instance.session = MagicMock()

        with patch("src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("src.config.owner.UserRepository", return_value=mock_user_repo):
                with patch("src.config.owner.AccountRepository", return_value=mock_acc_repo):
                    seed_owner()
                    mock_user_repo.create_user.assert_called_once()
                    mock_acc_repo.create_account.assert_called_once()


def test_seed_owner_skipped_when_email_already_registered():
    """Seeder must not proceed if email is taken by another role."""

    env = {
        "OWNER_EMAIL": "existing@test.com",
        "OWNER_USERNAME": "owner",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_role.return_value = []
        mock_user_repo.find_by_email.return_value = MagicMock()

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)
        mock_db_instance.session = MagicMock()

        with patch("src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("src.config.owner.UserRepository", return_value=mock_user_repo):
                with patch("src.config.owner.AccountRepository"):
                    seed_owner()
                    mock_user_repo.create_user.assert_not_called()


def test_seed_owner_skipped_when_username_already_taken():
    """Seeder must not proceed if username is already in use."""

    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "taken_username",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_role.return_value = []
        mock_user_repo.find_by_email.return_value = None

        mock_acc_repo = MagicMock()
        mock_acc_repo.find_by_username.return_value = MagicMock()

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)
        mock_db_instance.session = MagicMock()

        with patch("src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("src.config.owner.UserRepository", return_value=mock_user_repo):
                with patch("src.config.owner.AccountRepository", return_value=mock_acc_repo):
                    seed_owner()
                    mock_user_repo.create_user.assert_not_called()
