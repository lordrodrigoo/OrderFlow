#pylint: disable=redefined-builtin
from decimal import Decimal

class OrderItem:
    def __init__(
        self,
        id: int,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price: Decimal,
        subtotal: Decimal,
        total_price: Decimal
    ) -> None:
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal
        self.total_price = total_price
