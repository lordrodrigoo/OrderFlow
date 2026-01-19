from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    DELIVERED = "delivered"
    CANCELED = "canceled"

@dataclass
class Order:
    """Entity of domain - it represents an order in the system."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    total_amount: float
    delivery_fee: float
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: OrderStatus

    @property
    def is_delivered(self) -> bool:
        """Check if the order is delivered."""
        return self.status == OrderStatus.DELIVERED

    @property
    def is_canceled(self) -> bool:
        """Check if the order is canceled."""
        return self.status == OrderStatus.CANCELED

    @property
    def is_pending(self) -> bool:
        """Check if the order is pending."""
        return self.status == OrderStatus.PENDING

    @property
    def is_paid(self) -> bool:
        """Check if the order is paid."""
        return self.status == OrderStatus.PAID

    @property
    def summary(self) -> str:
        """Returns a summary of the order."""
        return f"Order {self.id}: {self.status.value} - Total: ${self.total_amount:.2f}"

    @property
    def scheduled_info(self) -> str:
        """Returns scheduled date information."""
        if self.scheduled_date:
            return f"Scheduled for {self.scheduled_date.strftime('%Y-%m-%d %H:%M:%S')}"
        return "No scheduled date"

    @staticmethod
    def create_order(
        user_id: int,
        address_id: int,
        total_amount: float,
        delivery_fee: float,
        notes: Optional[str],
        scheduled_date: Optional[datetime],
        status: OrderStatus
    ) -> 'Order':
        """Factory method to create a new order instance."""
        return Order(
            user_id=user_id,
            address_id=address_id,
            total_amount=total_amount,
            delivery_fee=delivery_fee,
            notes=notes,
            scheduled_date=scheduled_date,
            status=status
        )

    @staticmethod
    def from_entity(entity) -> 'Order':
        """Converts an OrderEntity to an Order domain model."""
        return Order(
            id=entity.id,
            user_id=entity.user_id,
            address_id=entity.address_id,
            total_amount=entity.total_amount,
            delivery_fee=entity.delivery_fee,
            notes=entity.notes,
            scheduled_date=entity.scheduled_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            status=OrderStatus(entity.status)
        )
