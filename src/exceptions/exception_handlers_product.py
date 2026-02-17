# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder



class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID: '{product_id}' not found."
        super().__init__(self.message)


async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": exc.message})
    )


class ProductFieldRequiredException(Exception):
    def __init__(self, field: str):
        self.field = field
        self.message = f"Field '{field}' is required."
        super().__init__(self.message)


async def product_field_required_exception_handler(request: Request, exc: RequestValidationError):
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
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"message": details})
    )


class ProductAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
        self.message = f"Product with name: '{name}' already exists."
        super().__init__(self.message)


async def product_already_exists_exception_handler(request: Request, exc: ProductAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({"message": exc.message})
    )


class ProductCategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        self.message = f"Category with ID: '{category_id}' not found."
        super().__init__(self.message)


async def product_category_not_found_exception_handler(request: Request, exc: ProductCategoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": exc.message})
    )



class InvalidPriceProductException(Exception):
    def __init__(self):
        self.message = "Price must be greater than zero."
        super().__init__(self.message)


async def invalid_price_product_exception_handler(request: Request, exc: InvalidPriceProductException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=jsonable_encoder({"message": exc.message})
    )
