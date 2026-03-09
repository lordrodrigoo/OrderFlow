# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse



class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID: '{product_id}' not found."
        super().__init__(self.message)


async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class ProductAlreadyExistsException(Exception):
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.message = f"Product with name: '{product_name}' already exists."
        super().__init__(self.message)


async def product_already_exists_exception_handler(request: Request, exc: ProductAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )


class ProductCategoryNotFoundException(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id
        self.message = f"Category with ID: '{category_id}' not found."
        super().__init__(self.message)


async def product_category_not_found_exception_handler(request: Request, exc: ProductCategoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )



class InvalidPriceProductException(Exception):
    def __init__(self):
        self.message = "Price must be greater than zero."
        super().__init__(self.message)


async def invalid_price_product_exception_handler(request: Request, exc: InvalidPriceProductException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": exc.message}
    )
