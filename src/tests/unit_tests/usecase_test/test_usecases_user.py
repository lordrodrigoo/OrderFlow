#pylint: disable=unused-argument
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from src.domain.models.user import UserRole, Users
from src.dto.request.user_request import UserRequest
from src.dto.response.user_response import UserResponse
from src.exceptions.exception_handlers_user import (
    UserNotFoundException,
    UserPermissionDeniedException,
    EmailAlreadyExistsException
)
from src.exceptions.exception_handlers_account import UsernameAlreadyExistsException
from src.exceptions.exception_handlers_auth import AdminForbiddenException, OwnerForbiddenException


def test_get_user_by_id_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(UserNotFoundException):
        usecase.get_user_by_id(999)


def test_delete_user_raises_404_when_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    current_user = MagicMock()
    current_user.id = 1
    current_user.role = UserRole.ADMIN
    with pytest.raises(UserNotFoundException):
        usecase.delete_user(999, current_user)


def test_update_user_permission_denied(usecase, user_repository_mock, valid_user_data, fake_admin_user):
    fake_admin_user.role = UserRole.USER
    fake_admin_user.id = 1
    request = UserRequest(**valid_user_data)
    with pytest.raises(UserPermissionDeniedException):
        usecase.update_user(999, request, fake_admin_user)



def test_create_user_email_exists(usecase, user_repository_mock, valid_user_data):
    user_repository_mock.find_by_email.return_value = user_repository_mock.create_user.return_value
    request = UserRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException) as exc_info:
        usecase.create_user(request)
    assert valid_user_data["email"] in exc_info.value.message


def test_create_user_username_exists(usecase, user_repository_mock, account_repository_mock, valid_user_data):
    user_repository_mock.find_by_email.return_value = None
    account_repository_mock.find_by_username.return_value = MagicMock()
    request = UserRequest(**valid_user_data)
    with pytest.raises(UsernameAlreadyExistsException) as exc_info:
        usecase.create_user(request)
    assert valid_user_data["username"] in exc_info.value.message


def test_verify_admin_raises_forbidden_for_non_admin(usecase, fake_user):
    fake_user.role = UserRole.USER
    non_admin = UserResponse(
        id=1, first_name="Ana", last_name="Silva", age=25,
        email="ana@test.com", phone="11999999999",
        is_active=True, role=UserRole.USER,
        created_at="2024-01-01T00:00:00"
    )
    with pytest.raises(AdminForbiddenException):
        usecase.verify_admin(non_admin)


def test_verify_admin_returns_user_for_admin(usecase):
    admin = UserResponse(
        id=2, first_name="Admin", last_name="User", age=30,
        email="admin@test.com", phone="11000000000",
        is_active=True, role=UserRole.ADMIN,
        created_at="2024-01-01T00:00:00"
    )
    result = usecase.verify_admin(admin)
    assert result == admin


def test_verify_admin_returns_user_for_owner(usecase):
    owner = UserResponse(
        id=3, first_name="System", last_name="Owner", age=30,
        email="owner@test.com", phone="11000000001",
        is_active=True, role=UserRole.OWNER,
        created_at="2024-01-01T00:00:00"
    )
    result = usecase.verify_admin(owner)
    assert result == owner


def test_get_total_users(usecase, user_repository_mock, fake_user):
    user_repository_mock.find_all_users.return_value = [fake_user, fake_user]
    total = usecase.get_total_users()
    assert total == 2


def test_get_user_by_email_not_found(usecase, user_repository_mock):
    user_repository_mock.find_by_email.return_value = None
    with pytest.raises(UserNotFoundException) as exc_info:
        usecase.get_user_by_email("notfound@example.com")
    assert "notfound@example.com" in exc_info.value.message


def test_update_user_not_found(usecase, user_repository_mock, valid_user_data, fake_admin_user):
    fake_admin_user.role = UserRole.ADMIN
    user_repository_mock.find_user_by_id.return_value = None
    request = UserRequest(**valid_user_data)
    with pytest.raises(UserNotFoundException):
        usecase.update_user(999, request, fake_admin_user)


def test_update_me_not_found(usecase, user_repository_mock, valid_user_data, fake_user):
    user_repository_mock.find_user_by_id.return_value = None
    request = UserRequest(**valid_user_data)
    with pytest.raises(UserNotFoundException):
        usecase.update_me(request, fake_user)


def test_list_users_by_name(usecase, user_repository_mock, fake_user):
    user_repository_mock.find_by_name.return_value = [fake_user]
    usecase.list_users(name="Rodrigo")
    user_repository_mock.find_by_name.assert_called_once_with("Rodrigo")


def test_list_users_filter_by_active(usecase, user_repository_mock, fake_user):
    fake_user.is_active = True
    user_repository_mock.find_all_users.return_value = [fake_user]
    result = usecase.list_users(active=True)
    assert all(u.is_active for u in result)


# --- verify_owner ---

def test_verify_owner_raises_for_user(usecase):
    user = UserResponse(
        id=1, first_name="Ana", last_name="Silva", age=25,
        email="ana@test.com", phone="11999999999",
        is_active=True, role=UserRole.USER,
        created_at="2024-01-01T00:00:00"
    )
    with pytest.raises(OwnerForbiddenException):
        usecase.verify_owner(user)


def test_verify_owner_raises_for_admin(usecase):
    admin = UserResponse(
        id=2, first_name="Admin", last_name="User", age=30,
        email="admin@test.com", phone="11000000000",
        is_active=True, role=UserRole.ADMIN,
        created_at="2024-01-01T00:00:00"
    )
    with pytest.raises(OwnerForbiddenException):
        usecase.verify_owner(admin)


def test_verify_owner_returns_user_for_owner(usecase):
    owner = UserResponse(
        id=3, first_name="System", last_name="Owner", age=30,
        email="owner@test.com", phone="11000000001",
        is_active=True, role=UserRole.OWNER,
        created_at="2024-01-01T00:00:00"
    )
    result = usecase.verify_owner(owner)
    assert result == owner


# --- update_user_role ---

def _make_owner():
    return UserResponse(
        id=99, first_name="System", last_name="Owner", age=30,
        email="owner@test.com", phone="11000000001",
        is_active=True, role=UserRole.OWNER,
        created_at="2024-01-01T00:00:00"
    )


def test_update_user_role_promotes_to_admin(usecase, user_repository_mock, fake_user):
    fake_user.role = UserRole.USER
    updated = Users(
        id=1, first_name="Rodrigo", last_name="Souza", age=30,
        phone="11999999999", email="rodrigo@test.com",
        is_active=True, role=UserRole.ADMIN, created_at=datetime.now()
    )
    user_repository_mock.find_user_by_id.return_value = fake_user
    user_repository_mock.update_user.return_value = updated

    result = usecase.update_user_role(1, UserRole.ADMIN, _make_owner())
    assert result.role == UserRole.ADMIN


def test_update_user_role_demotes_to_user(usecase, user_repository_mock, fake_user):
    fake_user.role = UserRole.ADMIN
    updated = Users(
        id=1, first_name="Rodrigo", last_name="Souza", age=30,
        phone="11999999999", email="rodrigo@test.com",
        is_active=True, role=UserRole.USER, created_at=datetime.now()
    )
    user_repository_mock.find_user_by_id.return_value = fake_user
    user_repository_mock.update_user.return_value = updated

    result = usecase.update_user_role(1, UserRole.USER, _make_owner())
    assert result.role == UserRole.USER


def test_update_user_role_blocked_for_non_owner(usecase, user_repository_mock, fake_user):
    admin = UserResponse(
        id=2, first_name="Admin", last_name="User", age=30,
        email="admin@test.com", phone="11000000000",
        is_active=True, role=UserRole.ADMIN,
        created_at="2024-01-01T00:00:00"
    )
    with pytest.raises(OwnerForbiddenException):
        usecase.update_user_role(1, UserRole.ADMIN, admin)


def test_update_user_role_cannot_assign_owner(usecase, user_repository_mock):
    with pytest.raises(OwnerForbiddenException):
        usecase.update_user_role(1, UserRole.OWNER, _make_owner())


def test_update_user_role_raises_when_user_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(UserNotFoundException):
        usecase.update_user_role(999, UserRole.ADMIN, _make_owner())
