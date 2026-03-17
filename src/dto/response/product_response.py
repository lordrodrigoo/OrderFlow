from datetime import datetime
from decimal import Decimal
from src.dto.base import BaseResponse


class ProductResponse(BaseResponse):
    id: int
    category_id: int
    name: str
    description: str
    price: Decimal
    is_available: bool
    preparation_time: int
    created_at: datetime
