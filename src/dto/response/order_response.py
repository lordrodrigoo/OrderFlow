from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dto.base import BaseResponse
from src.domain.models.order import OrderStatus

class OrderResponse(BaseResponse):
    id: int
    user_id: int
    address_id: int
    total_amount: Decimal
    delivery_fee: Decimal
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    status: OrderStatus
    created_at: datetime
