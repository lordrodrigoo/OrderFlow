# pylint: disable=unused-argument, redefined-outer-name
from fastapi import Request, status
from fastapi.responses import JSONResponse


class OrderItemNotFoundException(Exception):
    def __init__(self, order_item_id: int):
        self.order_item_id = order_item_id
        self.message = f"Order item with ID: '{order_item_id}' not found."
        super().__init__(self.message)


async def order_item_not_found_exception_handler(request: Request, exc: OrderItemNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class InvalidOrderItemException(Exception):
    def __init__(self, order_id: int, status: str):
        self.order_id = order_id
        self.status = status
        self.message = f"Cannot add items to order ID: '{order_id}' with status: '{status}'."
        super().__init__(self.message)


async def invalid_order_item_exception_handler(request: Request, exc: InvalidOrderItemException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message}
    )




class DuplicateOrderItemException(Exception):
    def __init__(self, order_id: int, product_id: int):
        self.order_id = order_id
        self.product_id = product_id
        self.message = f"Product '{product_id}' is already associated with order '{order_id}'."
        super().__init__(self.message)

async def duplicate_order_item_exception_handler(request: Request, exc: DuplicateOrderItemException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message}
    )
