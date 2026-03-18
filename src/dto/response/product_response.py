from datetime import datetime
from decimal import Decimal
from typing import Optional
from src.dto.base import BaseResponse


class ProductResponse(BaseResponse):
    id: int
    category_id: int
    name: str
    description: str
    price: Decimal
    is_available: bool
    preparation_time: Optional[int] = None
    image_url: Optional[str] = None
    preparation_time: int
    created_at: datetime
