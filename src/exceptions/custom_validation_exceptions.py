# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError



async def pydantic_validation_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    message = error["msg"].replace("Value error, ", "")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": message},
    )
