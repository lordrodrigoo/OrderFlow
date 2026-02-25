from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: str
    price: Decimal
    is_available: bool
    preparation_time: int
    created_at: datetime

    model_config = {"from_attributes": True}
