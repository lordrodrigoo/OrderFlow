#pylint: disable=unused-argument
from datetime import datetime
import pytest
from pydantic import ValidationError
from src.domain.models.user import UserRole
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


def test_update_user(usecase, user_repository_mock, user_response_mock):

    user_repository_mock.find_user_by_id.return_value = user_response_mock

    # Create a request object with updated data
    update_data = {
        "first_name": "RodrigoAtualizado",
        "last_name": "SouzaAtualizado",
        "age": 31,
        "email": "rodrigo.souza.atualizado@example.com",
        "phone": "11999999998",
        "username": "rodrigo.souza",
        "password": "@1234StrongPass",
        "role": "admin"
    }
    request = CreateUserRequest(**update_data)

    # Update the response mock to reflect the updated data
    user_response_mock.first_name = update_data["first_name"]
    user_response_mock.last_name = update_data["last_name"]
    user_response_mock.age = update_data["age"]
    user_response_mock.email = update_data["email"]
    user_response_mock.phone = update_data["phone"]
    user_response_mock.role = UserRole(update_data["role"])

    user_repository_mock.update_user.return_value = user_response_mock
    response = usecase.update_user(1, request)

    assert response.first_name == update_data["first_name"]
    assert response.email == update_data["email"]
    assert response.role == UserRole(update_data["role"])



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


def test_list_user_pagination_and_filters(usecase, user_repository_mock):
    user_repository_mock.list_users.return_value = [
        UserResponse(
            id=1,
            first_name="João",
            last_name="Silva",
            age=30,
            email="joao.silva@example.com",
            phone="1234567890",
            role=UserRole.USER,
            is_active=True,
            created_at=datetime.now()
        ),
        UserResponse(
            id=2,
            first_name="Maria",
            last_name="Souza",
            age=25,
            email="maria.souza@example.com",
            phone="0987654321",
            role=UserRole.ADMIN,
            is_active=True,
            created_at=datetime.now()
        ),
    ]


def test_get_user_by_id_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    response = usecase.get_user_by_id(999)
    assert response is None


def test_delete_user_not_found(usecase, user_repository_mock):
    user_repository_mock.find_user_by_id.return_value = None
    result = usecase.delete_user(999)
    assert result is False


def test_delete_user(usecase, user_repository_mock, user_response_mock):
    user_repository_mock.find_user_by_id.return_value = user_response_mock
    result = usecase.delete_user(1)
    assert result is True
