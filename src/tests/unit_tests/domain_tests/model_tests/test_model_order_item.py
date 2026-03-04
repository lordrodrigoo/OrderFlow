from decimal import Decimal
from src.domain.models.order_item import OrderItem
from src.domain.models.order_item import OrderItem

def test_create_order_item():
    order_item = OrderItem.create_order_item(
        order_id=1,
        product_id=2,
        quantity=3,
        unit_price=9.99,
        notes="Extra frosting"
    )
    assert isinstance(order_item, OrderItem)
    assert order_item.order_id == 1
    assert order_item.product_id == 2
    assert order_item.quantity == 3
    assert order_item.unit_price == 9.99
    assert order_item.notes == "Extra frosting"



def test_total_price_property():
    item = OrderItem(
        order_id=1,
        product_id=2,
        quantity=3,
        unit_price=Decimal('10.00'),
        subtotal=Decimal('30.00')
    )
    assert item.total_price == Decimal('30.00')
    item_wrong = OrderItem(
        order_id=1,
        product_id=2,
        quantity=3,
        unit_price=Decimal('10.00'),
        subtotal=Decimal('999.99')
    )
    assert item_wrong.total_price == Decimal('30.00')

def test_create_order_item_factory():
    item = OrderItem.create_order_item(
        order_id=1,
        product_id=2,
        quantity=4,
        unit_price=Decimal('5.50'),
        notes="Sem cebola"
    )
    assert item.subtotal == Decimal('22.00')
    assert item.total_price == Decimal('22.00')
    assert item.notes == "Sem cebola"


def test_from_entity():
    class MockOrderItemEntity:
        def __init__(self):
            self.id = 1
            self.order_id = 1
            self.product_id = 2
            self.quantity = 3
            self.unit_price = Decimal('9.99')
            self.subtotal = Decimal('29.97')
            self.notes = "Extra frosting"
            self.created_at = None
            self.updated_at = None

    entity = MockOrderItemEntity()
    order_item = OrderItem.from_entity(entity)
    assert order_item.id == 1
    assert order_item.order_id == 1
    assert order_item.product_id == 2
    assert order_item.quantity == 3
    assert order_item.unit_price == Decimal('9.99')
    assert order_item.subtotal == Decimal('29.97')
    assert order_item.notes == "Extra frosting"
    assert order_item.created_at is None
