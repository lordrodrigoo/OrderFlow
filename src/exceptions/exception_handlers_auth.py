# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse


class TokenExpiredException(Exception):
    def __init__(self, message: str = "Token has expired"):
        self.message = message
        super().__init__(message)


async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message}
    )


class TokenInvalidException(Exception):
    def __init__(self, message: str = "Invalid token"):
        self.message = message
        super().__init__(message)


async def token_invalid_exception_handler(request: Request, exc: TokenInvalidException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message}
    )


class InvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid username or password"):
        self.message = message
        super().__init__(message)


async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": exc.message}
    )
