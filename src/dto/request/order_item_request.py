from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class OrderItemRequest(BaseModel):
    order_id: int = Field(
        ...,
        gt=0,
        description="..."
    )
    product_id: int = Field(
        ...,
        gt=0,
        description="..."
    )
    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity of the product, must be greater than 0"
    )
    unit_price: Decimal = Field(
        ...,
        gt=0,
        le=100000,
        decimal_places=2,
        description="Unit price of the product, must be greater than 0"
    )
    notes: Optional[str] = Field(
        None,
        max_length=255,
        description="Additional notes for the order item, optional, max length 255 characters"
    )

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: Optional[str]) -> Optional[str]:
        if value and value.strip() == "":
            raise ValueError("Notes cannot be empty string")
        return value.strip() if value else value
