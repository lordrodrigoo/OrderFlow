# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class UsernameAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username


async def username_exception_handler(
        request: Request, exc: UsernameAlreadyExistsException
    ):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({
            "errors": {
                "username": f"The username '{exc.username}' is already registered."
            }
        }),
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
