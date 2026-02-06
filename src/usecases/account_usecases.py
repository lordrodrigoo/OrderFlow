from src.domain.repositories.account_repository import AccountRepositoryInterface
from src.domain.models.account import Account, AccountStatus
from src.dto.request.account_request import CreateAccountRequest
from src.dto.response.account_response import AccountResponse
from src.exceptions.exception_handlers import UsernameAlreadyExistsException

class CreateAccountUsecase:
    def __init__(self, account_repository: AccountRepositoryInterface):
        self.account_repository = account_repository

    def create_account(self, account_request: CreateAccountRequest) -> AccountResponse:
        if self.account_repository.find_by_username(account_request.username):
            raise UsernameAlreadyExistsException(username=account_request.username)

        account_entity = Account(
            user_id=account_request.user_id,
            username=account_request.username,
            password_hash=Account.hash_password(account_request.password),
            status=AccountStatus.ACTIVE
        )
        created_account = self.account_repository.create_account(account_entity)
        return AccountResponse.from_domain(created_account)
