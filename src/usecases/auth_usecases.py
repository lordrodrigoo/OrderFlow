from jose import jwt, JWTError
from src.domain.models.account import AccountStatus
from src.infra.db.repositories.account_user_repository_interface import AccountRepository
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.dto.response.token_response import TokenResponse
from src.config.security import  verify_password, create_access_token, DUMMY_HASH, SECRET_KEY, ALGORITHM

from src.exceptions.exception_handlers_account import (
    InvalidCredentialsException,
    AccountInactiveException
)

class AuthUseCases:
    def __init__(
            self,
            account_repository: AccountRepository,
            user_repository: UserRepository
        ):
        self.account_repository = account_repository
        self.user_repository = user_repository


    def login(self, username: str, password: str) -> TokenResponse:
        account = self.account_repository.find_by_username(username)

        if not account:
            verify_password(password, DUMMY_HASH)
            raise InvalidCredentialsException()

        if account.status != AccountStatus.ACTIVE:
            raise AccountInactiveException(account_id=account.id)

        if not verify_password(password, account.password_hash):
            raise InvalidCredentialsException()

        user = self.user_repository.find_user_by_id(account.user_id)
        if not user:
            raise InvalidCredentialsException()

        token = create_access_token({
            "sub": str(user.email),
            "user_id": str(user.id),
            "role": user.role.value
        })
        refresh_token = self.refresh_token({
            "sub": str(user.email),
            "user_id": str(user.id),
            "role": user.role.value
        })
        return TokenResponse(access_token=token, token_type="bearer", refresh_token=refresh_token)


    def refresh_token(self, refresh_token: str) -> TokenResponse:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
        except JWTError as exc:
            raise InvalidCredentialsException() from exc

        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            raise InvalidCredentialsException()

        token = create_access_token({
            "sub": str(user.email),
            "user_id": str(user.id),
            "role": user.role.value
        })
        return TokenResponse(access_token=token, token_type="bearer")
