from pydantic import BaseModel
from src.domain.models.order import OrderStatus


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus
