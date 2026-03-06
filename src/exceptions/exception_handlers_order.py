# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse


class OrderNotFoundException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.message = f"Order with ID: '{order_id}' not found."
        super().__init__(self.message)

async def order_not_found_exception_handler(request: Request, exc: OrderNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class OrderAlreadyCanceledException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.message = f"Order with ID: '{order_id}' is already canceled."
        super().__init__(self.message)

async def order_already_canceled_exception_handler(request: Request, exc: OrderAlreadyCanceledException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )
