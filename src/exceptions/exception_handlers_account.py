# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class UsernameAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"The username '{username}' is already registered."
        super().__init__(self.message)


async def username_exception_handler(request: Request, exc: UsernameAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({"message": exc.message})
    )


class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Invalid username or password."
        super().__init__(self.message)


async def invalid_credentials_exception_handler(
        request: Request, exc: InvalidCredentialsException
    ):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({"message": exc.message}),
    )


class AccountNotFoundException(Exception):
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.message = f"Account with ID '{account_id}' not found."
        super().__init__(self.message)


async def account_not_found_exception_handler(
        request: Request, exc: AccountNotFoundException
    ):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": exc.message}),
    )


class AccountInactiveException(Exception):
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.message = f"Account with ID '{account_id}' is inactive."
        super().__init__(self.message)


async def account_inactive_exception_handler(
        request: Request, exc: AccountInactiveException
    ):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({"message": exc.message}),
    )


class AccountPermissionDeniedException(Exception):
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.message = f"Permission denied for account with ID '{account_id}'."
        super().__init__(self.message)

async def account_permission_denied_exception_handler(
        request: Request, exc: AccountPermissionDeniedException
    ):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder({"message": exc.message}),
    )
