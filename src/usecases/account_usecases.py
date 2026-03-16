import logging
from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus
from src.dto.request.account_request import AccountRequest, UpdateAccountRequest, UpdatePasswordRequest
from src.dto.response.account_response import AccountResponse
from src.dto.response.user_response import UserResponse
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.config.security import hash_password, verify_password

from src.exceptions.exception_handlers_account import (
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    AccountNotFoundException,
    AccountPermissionDeniedException
)

logger = logging.getLogger(__name__)


class AccountUsecase:
    def __init__(self,
                account_repository: AccountRepositoryInterface,
                user_repository: UserRepositoryInterface
            ):
        self.account_repository = account_repository
        self.user_repository = user_repository

    def create_account(self, account_request: AccountRequest) -> AccountResponse:
        if self.account_repository.find_by_username(account_request.username):
            logger.warning("Username already exists", extra={"username": account_request.username})
            raise UsernameAlreadyExistsException(username=account_request.username)

        account_entity = Account(
            user_id=account_request.user_id,
            username=account_request.username,
            password_hash=hash_password(account_request.password),
            status=AccountStatus.ACTIVE
        )
        created_account = self.account_repository.create_account(account_entity)
        logger.info("Account created", extra={"account_id": created_account.id})
        return AccountResponse(**created_account.__dict__)


    def get_authenticated_user(self, email: str) -> UserResponse:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise InvalidCredentialsException()
        return UserResponse(**user.__dict__)


    def get_account_by_id(self, account_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            logger.warning("Account not found", extra={"account_id": account_id})
            raise AccountNotFoundException(account_id=account_id)
        return AccountResponse(**account.__dict__)



    def update_account(self,
                    account_id: int,
                    account_request: UpdateAccountRequest,
                    current_user_id: int
    ) -> AccountResponse:

        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            raise AccountPermissionDeniedException(account_id=account_id)

        if self.account_repository.find_by_username(account_request.username):
            raise UsernameAlreadyExistsException(username=account_request.username)

        account.username = account_request.username
        updated_account = self.account_repository.update_account(account)
        logger.info("Account updated", extra={"account_id": account_id})
        return AccountResponse(**updated_account.__dict__)


    def update_password(self,
                    account_id: int,
                    password_request: UpdatePasswordRequest,
                    current_user_id: int
    ) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            raise AccountPermissionDeniedException(account_id=account_id)

        if not verify_password(password_request.current_password, account.password_hash):
            logger.warning("Invalid current password", extra={"account_id": account_id})
            raise InvalidCredentialsException()

        new_password_hash = hash_password(password_request.new_password)
        updated = self.account_repository.update_password(account_id, new_password_hash)
        logger.info("Password updated", extra={"account_id": account_id})
        return AccountResponse(**updated.__dict__)


    def suspend_account(self, account_id: int, current_user_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            raise AccountPermissionDeniedException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.SUSPENDED)
        logger.info("Account suspended", extra={"account_id": account_id})
        return AccountResponse(**updated.__dict__)


    def inactivate_account(self, account_id: int, current_user_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            raise AccountPermissionDeniedException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.INACTIVE)
        logger.info("Account inactivated", extra={"account_id": account_id})
        return AccountResponse(**updated.__dict__)


    def activate_account(self, account_id: int, current_user_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            raise AccountPermissionDeniedException(account_id=account_id)

        updated = self.account_repository.update_status(account_id, AccountStatus.ACTIVE)
        logger.info("Account activated", extra={"account_id": account_id})
        return AccountResponse(**updated.__dict__)


    def delete_account(self, account_id: int, current_user_id: int) -> AccountResponse:
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            logger.warning("Account not found for deletion", extra={"account_id": account_id})
            raise AccountNotFoundException(account_id=account_id)

        if account.user_id != current_user_id:
            logger.warning("Permission denied to delete account", extra={"account_id": account_id})
            raise AccountPermissionDeniedException(account_id=account_id)

        self.account_repository.delete_account(account_id)
        logger.info("Account deleted", extra={"account_id": account_id})
        return AccountResponse(**account.__dict__)
