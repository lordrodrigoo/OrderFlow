from decimal import Decimal
import pytest
from src.infra.db.entities.order_item import OrderItemEntity




@pytest.fixture
def fake_order_item(db_session, fake_order, fake_product):
    order_item = OrderItemEntity(
        order_id=fake_order.id,
        product_id=fake_product.id,
        quantity=2,
        unit_price=Decimal('25.50'),
        subtotal=Decimal('51.00'),
        notes="Handle with care"
    )
    db_session.add(order_item)
    db_session.commit()
    return order_item


@pytest.fixture
def valid_order_item_data(fake_order, fake_product):
    return {
        "order_id": fake_order.id,
        "product_id": fake_product.id,
        "quantity": 2,
        "unit_price": float('25.50'),
        "subtotal": float('51.00'),
        "notes": "Handle with care"
    }
