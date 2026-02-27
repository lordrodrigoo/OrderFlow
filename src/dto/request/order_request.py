from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator



class OrderRequest(BaseModel):
    address_id: int = Field(
        ...,
        gt=0,
        description="...")
    total_amount: Decimal = Field(
        ...,
        gt=0, # don't allow zero or negative total amount
        le=100000,  # max limit for total amount
        decimal_places=2,  # It's assurance that the total amount has at most two decimal
        description="Total amount of the order, must be greater than 0"
    )
    delivery_fee: Decimal = Field(
        ...,
        ge=0,  # don't allow negative delivery fee
        le=10000,  # max limit for delivery fee
        decimal_places=2,  # It's assurance that the delivery fee has at most two decimal
        description="Delivery fee of the order, must be greater than or equal to 0"
    )
    notes: Optional[str] = Field(
        None,
        max_length=255,
        description="Additional notes for the order, optional, max length 255 characters"
    )
    scheduled_date: Optional[datetime] = Field(
        None,
        description="Scheduled delivery date for the order, optional, must be a valid date"
    )


    @field_validator("scheduled_date")
    @classmethod
    def validate_scheduled_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value:
            now = datetime.now()
            if value < now:
                raise ValueError("Scheduled date must be in the future")
            if value > now + timedelta(days=30):
                raise ValueError("Scheduled date cannot be more than 30 days in the future")
        return value


    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: Optional[str]) -> Optional[str]:
        if value and value.strip() == "":
            raise ValueError("Notes cannot be empty string")
        return value.strip() if value else value
