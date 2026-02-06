import pytest
from pydantic import ValidationError
from src.dto.request.user_request import CreateUserRequest
from src.dto.response.user_response import UserResponse
from src.exceptions.exception_handlers import EmailAlreadyExistsException


def test_create_user_success(
        usecase,
        user_repository_mock,
        valid_user_data
    ):

    user_repository_mock.find_by_email.return_value = None
    request = CreateUserRequest(**valid_user_data)
    response = usecase.create_user(request)

    assert isinstance(response, UserResponse)
    assert response.first_name == valid_user_data["first_name"]
    assert response.email == valid_user_data["email"]
    assert response.role.value == valid_user_data["role"]


def test_create_user_email_exists(usecase, user_repository_mock, valid_user_data):
    user_repository_mock.find_by_email.return_value = user_repository_mock.create_user.return_value  # Simula e-mail já cadastrado
    request = CreateUserRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException):
        usecase.create_user(request)


def test_create_user_invalid_request():
    with pytest.raises(ValidationError):
        CreateUserRequest(
            first_name="J0ao",
            last_name="Silva",
            age=15,
            email="emailinvalido",
            phone="abc",
            username="js",
            password="fraca",
            role="user"
        )
