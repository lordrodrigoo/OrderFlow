from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime



@dataclass
class OrderItem:
    """Entity of domain - it represents an item in an order."""
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    notes: Optional[str] = None
    id: Optional[int] = None
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    created_at: Optional[datetime] = None

    @property
    def total_price(self) -> Decimal:
        """Calculate total price for the order item."""
        return self.unit_price * self.quantity

    @staticmethod
    def create_order_item(
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price: Decimal,
        notes: Optional[str] = None
    ) -> 'OrderItem':
        """Factory method to create a new OrderItem."""
        subtotal = unit_price * quantity
        return OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            notes=notes
        )

    @staticmethod
    def from_entity(entity) -> 'OrderItem':
        """Converts an OrderItemEntity to an OrderItem domain model."""
        return OrderItem(
            id=entity.id,
            order_id=entity.order_id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            unit_price=entity.unit_price,
            subtotal=entity.subtotal,
            notes=entity.notes,
            created_at=entity.created_at
        )
