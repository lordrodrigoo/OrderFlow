from typing import Dict
from src.dto.base import BaseResponse


class DashboardResponse(BaseResponse):
    total_orders: int
    total_users: int
    total_products: int
    total_revenue: float
    orders_by_status: Dict[str, int]
