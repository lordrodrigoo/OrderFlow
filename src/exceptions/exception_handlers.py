# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email

class InvalidCredentialsException(Exception):
    pass

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


async def email_exception_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({
            "errors": {
                "email": f"The email '{exc.email}' is already registered."
            }
        }),
    )

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({
            "errors": {
                "auth": "Invalid username or password."
            }
        }),
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        message = error["msg"]
        if field == "email":
            message = "invalid email address"
        details.append({
            "field": field,
            "message": message,
            "type": error["type"],
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"errors": details}),
    )
