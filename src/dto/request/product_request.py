import re
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


PRODUCT_NAME_PATTERN = re.compile(r'^[A-Za-zÀ-ÿ0-9\s\-]+$')



class ProductRequest(BaseModel):
    category_id: int = Field(
        ...,
        description="ID of the category the product belongs to"
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="product name, ex: 'Coca-Cola 2L'",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="product description, ex: 'Refreshing beverage with a hint of lemon'",
    )
    price: Decimal = Field(
        ...,
        ge=0,  # don't allow negative prices
        le=10000,  # max limit for price
        decimal_places=2,  # It's assurance that the price has at most two decimal places
        description="price of the product, ex: 9.99",
    )
    is_available: bool = Field(
        True,
        description="availability of the product, default is True",
    )
    preparation_time: int = Field(
        ...,
        ge=1,
        description="preparation time in minutes, ex: 15",
    )


    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not PRODUCT_NAME_PATTERN.match(value):
            raise ValueError("must contain only letters, numbers, hyphens or spaces.")
        return value
