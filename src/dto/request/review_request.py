from typing import Optional
from pydantic import BaseModel, Field, field_validator



class ReviewRequest(BaseModel):
    user_id: int = Field(..., gt=0, description='ID of the user creating the review')
    product_id: int = Field(..., gt=0, description='ID of the product being reviewed')
    rating: int | None = Field(
        None,
        ge=1,
        le=5,
        description="Rating should be between 1 and 5"
    )
    comment: str | None = Field(
        None,
        max_length=500,
        description="Comment should have at most 500 characters"
    )

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, value: str | None) -> str | None:
        if value and value.strip() == "":
            raise ValueError("Comment cannot be empty string")
        return value.strip() if value else value


class ReviewFilters(BaseModel):
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None
    skip: int = 0
    limit: int = 10
