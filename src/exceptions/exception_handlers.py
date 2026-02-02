# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email

async def email_exception_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({
            "success": False,
            "error": {
                "type": "EmailAlreadyExists",
                "message": f"The email {exc.email} already exists."
            }
        }),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {
            "field": ".".join(str(loc) for loc in error["loc"] if loc != "body"),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({
            "success": False,
            "error": {
                "type": "ValidationError",
                "details": details
            }
        }),
    )
