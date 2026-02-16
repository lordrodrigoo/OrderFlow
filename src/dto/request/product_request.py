from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class ProductRequest(BaseModel):
    category_id: int = Field(
        ...,
        description="ID of the category the product belongs to"
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="name must be between 3 and 100 characters",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="description must be between 10 and 500 characters",
    )
    price: Decimal = Field(
        ...,
        ge=0,  # don't allow negative prices
        le=10000,  # max limit for price
        decimal_places=2,  # It's assurance that the price has at most two decimal places
        description="price must be entre 0 e 10000, com até duas casas decimais",
    )
    is_available: bool = Field(
        True,
        description="availability status of the product, default is True"
    )
    preparation_time: int = Field(
        ...,
        ge=1,
        description="preparation time in minutes, must be at least 1 minute",
    )


    @field_validator("name")
    @classmethod
    def name_must_be_alphanumeric(cls, name: str) -> str:
        if not name.isalpha():
            raise ValueError("name must contain only alphabetic characters")
        return name
