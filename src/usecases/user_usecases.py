from src.exceptions.exception_handlers import EmailAlreadyExistsException
from src.domain.models.user import Users
from src.dto.request.user_request import CreateUserRequest
from src.dto.response.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus


class CreateUserUsecase:
    def __init__(
            self, user_repository: UserRepositoryInterface,
            account_repository: AccountRepositoryInterface
        ):

        self.user_repository = user_repository
        self.account_repository = account_repository

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
        created_user = self.user_repository.create_user(user_entity)

        # Creating account vinculated to user
        account_entity = Account(
            user_id=created_user.id,
            username=user_request.username,
            password_hash=Account.hash_password(user_request.password),
            status=AccountStatus.ACTIVE
        )
        self.account_repository.create_account(account_entity)

        return UserResponse(**created_user.__dict__)
