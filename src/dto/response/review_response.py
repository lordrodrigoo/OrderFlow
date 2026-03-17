from datetime import datetime
from pydantic import Field
from src.dto.base import BaseResponse


class ReviewResponse(BaseResponse):
    id: int
    rating: int | None = Field(
        None,
        ge=0,
        le=5,
        description="Rating should be between 0 and 5"
    )
    comment: str | None = Field(
        None,
        max_length=500,
        description="Comment should have at most 500 characters"
    )
    created_at: datetime
    user_id: int
    product_id: int
