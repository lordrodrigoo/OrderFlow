import re
from pydantic import BaseModel, Field, field_validator

CATEGORY_NAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9\s\-]+$')

class CategoryRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="category name, ex: 'Cakes'",
    )
    description: str = Field(
        None,
        min_length=10,
        max_length=50,
        description="category description, ex: 'Delicious cakes for every occasion'",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not CATEGORY_NAME_PATTERN.match(value):
            raise ValueError("must contain only letters, numbers, hyphens or spaces.")
        return value
