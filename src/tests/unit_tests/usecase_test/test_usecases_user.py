#pylint: disable=unused-argument
import pytest
from src.domain.models.user import UserRole
from src.dto.request.user_request import UserRequest
from src.exceptions.exception_handlers_user import (
    UserNotFoundException,
    UserPermissionDeniedException,
    EmailAlreadyExistsException
)




def test_get_user_by_id_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(UserNotFoundException):
        usecase.get_user_by_id(999)


def test_delete_user_raises_404_when_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    with pytest.raises(UserNotFoundException):
        usecase.delete_user(999)


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
