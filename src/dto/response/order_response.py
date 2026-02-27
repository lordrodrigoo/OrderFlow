from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from src.domain.models.order import OrderStatus

class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: int
    total_amount: Decimal
    delivery_fee: Decimal
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}
