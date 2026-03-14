from src.domain.models.user import Users, UserRole
from src.dto.request.user_request import UserRequest
from src.dto.response.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus
from src.config.security import hash_password

from src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException,
    UserNotFoundException,
    UserPermissionDeniedException
)
from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
)



class UserUsecase:
    def __init__(
            self, user_repository: UserRepositoryInterface,
            account_repository: AccountRepositoryInterface
        ):

        self.user_repository = user_repository
        self.account_repository = account_repository

    def create_user(self, user_request: UserRequest) -> UserResponse:
        if self.user_repository.find_by_email(user_request.email):
            raise EmailAlreadyExistsException(email=user_request.email)

        if self.account_repository.find_by_username(user_request.username):
            raise UsernameAlreadyExistsException(username=user_request.username)


        user_entity = Users(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            age=user_request.age,
            phone=user_request.phone,
            email=user_request.email,
            is_active=True,
            role=user_request.role
        )
        created_user = self.user_repository.create_user(user_entity)

        # Creating account vinculated to user
        account_entity = Account(
            user_id=created_user.id,
            username=user_request.username,
            password_hash=hash_password(user_request.password),
            status=AccountStatus.ACTIVE
        )
        self.account_repository.create_account(account_entity)
        return UserResponse(**created_user.__dict__)


    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return UserResponse(**user.__dict__)


    def get_user_by_email(self, email: str) -> UserResponse:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundException(email=email)
        return UserResponse(**user.__dict__)


    def list_users(
        self,
        name: str = None,
        email: str = None,
        active: bool = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[UserResponse]:
        users = []

        if email:
            user = self.user_repository.find_by_email(email)
            if user:
                users = [user]
        elif name:
            users = self.user_repository.find_by_name(name)
        else:
            users = self.user_repository.find_all_users()

        # Additional filtering
        if active is not None:
            users = [user for user in users if getattr(user, 'is_active', None) == active]

        # Pagination
        users = users[skip: skip + limit] if users else []
        return [UserResponse(**user.__dict__) for user in users]


    def update_user(
            self,
            user_id: int,
            user_request: UserRequest,
            current_user: UserResponse
    ) -> UserResponse:

        if current_user.id != user_id and current_user.role != UserRole.ADMIN:
            raise UserPermissionDeniedException(user_id=user_id)

        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)

        user.first_name = user_request.first_name
        user.last_name = user_request.last_name
        user.age = user_request.age
        user.phone = user_request.phone
        user.email = user_request.email
        user.role = user_request.role

        updated_user = self.user_repository.update_user(user)
        return UserResponse(**updated_user.__dict__)


    def update_me(self, user_request: UserRequest, current_user: UserResponse) -> UserResponse:
        user = self.user_repository.find_user_by_id(current_user.id)
        if not user:
            raise UserNotFoundException(user_id=current_user.id)

        user.first_name = user_request.first_name
        user.last_name = user_request.last_name
        user.age = user_request.age
        user.phone = user_request.phone
        user.email = user_request.email

        updated_user = self.user_repository.update_user(user)
        return UserResponse(**updated_user.__dict__)


    def delete_user(self, user_id: int) -> bool:
        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        self.user_repository.delete_user(user_id)
        return True
