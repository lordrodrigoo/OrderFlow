# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError



class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"Email '{email}' already exists."
        super().__init__(self.message)


async def email_exception_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )



class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with ID: '{user_id}' not found."
        super().__init__(self.message)



async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )



class FieldRequiredException(Exception):
    def __init__(self, field: str):
        self.field = field
        self.message = f"Field '{field}' is required."
        super().__init__(self.message)


async def field_required_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")

        # Messages to required fields
        if error["type"] == "value_error.missing":
            message = f"Field '{field}' is required."
        elif error["type"] == "type_error.integer":
            message = f"Field '{field}' must be an integer."
        elif error["type"] == "type_error.string":
            message = f"Field '{field}' must be a string."
        else:
            message = error["msg"]
        details.append({"message": message})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": message, "details": details},
    )



class UserPermissionDeniedException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = "You do not have permission to update this user."
        super().__init__(self.message)


async def user_permission_denied_exception_handler(request: Request, exc: UserPermissionDeniedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': exc.message, 'user_id': exc.user_id}
    )
