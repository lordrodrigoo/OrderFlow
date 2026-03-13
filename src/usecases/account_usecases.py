from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus
from src.dto.request.account_request import AccountRequest, UpdateAccountRequest, UpdatePasswordRequest
from src.dto.response.account_response import AccountResponse
from src.dto.response.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.config.security import hash_password, verify_password, create_access_token, DUMMY_HASH
from src.dto.request.login_request import LoginRequest
from src.dto.response.token_response import TokenResponse

from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    AccountInactiveException,
    AccountNotFoundException,
    AccountPermissionDeniedException
)

class AccountUsecase:
    def __init__(self,
                account_repository: AccountRepositoryInterface,
                user_repository: UserRepositoryInterface
            ):
        self.account_repository = account_repository
        self.user_repository = user_repository

    def create_account(self, account_request: AccountRequest) -> AccountResponse:
        if self.account_repository.find_by_username(account_request.username):
            raise UsernameAlreadyExistsException(username=account_request.username)

        account_entity = Account(
            user_id=account_request.user_id,
            username=account_request.username,
            password_hash=hash_password(account_request.password),
            status=AccountStatus.ACTIVE
        )
        created_account = self.account_repository.create_account(account_entity)
        return AccountResponse(**created_account.__dict__)


    def login(self, login_request: LoginRequest) -> TokenResponse:
        account = self.account_repository.find_by_username(login_request.username)

        if not account:
            verify_password(login_request.password, DUMMY_HASH)
            raise InvalidCredentialsException()

        if account.status != AccountStatus.ACTIVE:
            raise AccountInactiveException(account_id=account.id)

        if not verify_password(login_request.password, account.password_hash):
            raise InvalidCredentialsException()

        user = self.user_repository.find_user_by_id(account.user_id)
        if not user:
            raise InvalidCredentialsException()

        token = create_access_token({
            "sub": str(user.email),
            "user_id": str(user.id),
            "role": user.role.value
        })
        return TokenResponse(access_token=token, token_type="bearer")


    def get_authenticated_user(self, email: str) -> UserResponse:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise InvalidCredentialsException()
        return UserResponse(**user.__dict__)


    def get_account_by_id(self, account_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)
        return AccountResponse(**account.__dict__)



    def update_account(self,
                    account_id: int,
                    account_request: UpdateAccountRequest,
                    current_user: UserResponse
    ) -> AccountResponse:

        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user.id:
            raise AccountPermissionDeniedException(account_id=account_id)

        if self.account_repository.find_by_username(account_request.username):
            raise UsernameAlreadyExistsException(username=account_request.username)

        account.username = account_request.username
        updated_account = self.account_repository.update_account(account)
        return AccountResponse(**updated_account.__dict__)


    def update_password(self,
                    account_id: int,
                    password_request: UpdatePasswordRequest,
                    current_user: UserResponse
    ) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user.id:
            raise AccountPermissionDeniedException(account_id=account_id)

        if not verify_password(password_request.current_password, account.password_hash):
            raise InvalidCredentialsException()

        new_password_hash = hash_password(password_request.new_password)
        updated = self.account_repository.update_password(account_id, new_password_hash)
        return AccountResponse(**updated.__dict__)


    def deactivate_account(self, account_id: int, current_user: UserResponse) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user.id:
            raise AccountPermissionDeniedException(account_id=account_id)
        updated = self.account_repository.update_status(account_id, AccountStatus.INACTIVE)
        return AccountResponse(**updated.__dict__)


    def suspend_account(self, account_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.SUSPENDED)
        return AccountResponse(**updated.__dict__)


    def inactivate_account(self, account_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.INACTIVE)
        return AccountResponse(**updated.__dict__)


    def activate_account(self, account_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.ACTIVE)
        return AccountResponse(**updated.__dict__)


    def delete_account(self, account_id: int, current_user: UserResponse) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user.id:
            raise AccountPermissionDeniedException(account_id=account_id)

        self.account_repository.delete_account(account_id)
        return AccountResponse(**account.__dict__)
