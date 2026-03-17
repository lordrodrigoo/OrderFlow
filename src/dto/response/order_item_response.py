from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dto.base import BaseResponse


class OrderItemResponse(BaseResponse):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    notes: Optional[str] = None
    created_at: datetime
