from src.exceptions.exception_handlers import EmailAlreadyExistsException
from src.domain.models.user import Users
from src.dto.request.user_request import CreateUserRequest
from src.dto.response.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface


class CreateUserUsecase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user_request: CreateUserRequest) -> UserResponse:
        if self.user_repository.find_by_email(user_request.email):
            raise EmailAlreadyExistsException(email=user_request.email)

        user_entity = Users(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            age=user_request.age,
            phone=user_request.phone,
            email=user_request.email,
            is_active=True
        )
        created_user = self.user_repository.create(user_entity)
        return UserResponse(**created_user)
