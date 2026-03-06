# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse


class CategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        self.message = f"Category with ID: '{category_id}' not found."
        super().__init__(self.message)

async def category_not_found_exception_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class CategoryAlreadyExistsException(Exception):
    def __init__(self, category_name: str):
        self.category_name = category_name
        self.message = f"Category with name: '{category_name}' already exists."
        super().__init__(self.message)

async def category_already_exists_exception_handler(request: Request, exc: CategoryAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )
