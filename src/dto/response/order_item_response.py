from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    notes: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
