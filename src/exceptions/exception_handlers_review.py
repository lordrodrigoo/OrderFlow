#pylint: disable=unused-argument
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import Request, status




class ReviewNotFoundException(Exception):
    def __init__(self, review_id: int, user_id: Optional[int] = None, product_id: Optional[int] = None):
        self.message = f"Review with ID: '{review_id}' not found."
        if user_id:
            self.message += f" [user_id={user_id}]"
        if product_id:
            self.message += f" [product_id={product_id}]"
        super().__init__(self.message)


async def review_not_found_exception_handler(request: Request, exc: ReviewNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class InvalidReviewException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

async def invalid_review_exception_handler(request: Request, exc: InvalidReviewException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message}
    )
