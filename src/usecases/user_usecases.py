from fastapi import HTTPException
from src.api.dtos.user_request import CreateUserRequest
from src.api.dtos.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.models.user import Users


class CreateUserUsecase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository


    def create_user(self, user_request: CreateUserRequest) -> UserResponse:
        if self.user_repository.find_by_email(user_request.email):
            raise HTTPException(status_code=409, detail="Email already exists")

        # Convert request DTO to domain model
        user_entity = Users(
            first_name = user_request.first_name,
            last_name = user_request.last_name,
            age = user_request.age,
            phone = user_request.phone,
            email = user_request.email,
            is_active = True
        )
        # Save user using the repository
        created_user = self.user_repository.create_user(user_entity)


        # Return response DTO
        return UserResponse.model_validate(created_user)
