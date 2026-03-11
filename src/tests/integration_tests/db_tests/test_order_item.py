#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from decimal import Decimal
import pytest
from src.infra.db.entities.order_item import OrderItemEntity


def test_create_order_item(db_session, fake_order_item, fake_order, fake_product):
    assert fake_order_item.id is not None
    assert fake_order_item.quantity == 2
    assert fake_order_item.unit_price == Decimal('25.50')
    assert fake_order_item.subtotal == Decimal('51.00')
    assert fake_order_item.notes == "Handle with care"

def test_update_order_item(db_session, fake_order_item):
    fake_order_item.quantity = 3
    fake_order_item.subtotal = Decimal('39.90')
    fake_order_item.unit_price = Decimal('13.30')
    fake_order_item.notes = "Updated notes"
    db_session.commit()
    updated_order_item = db_session.query(OrderItemEntity).filter_by(id=fake_order_item.id).first()
    assert updated_order_item.quantity == 3
    assert updated_order_item.subtotal == Decimal('39.90')
    assert updated_order_item.unit_price == Decimal('13.30')
    assert updated_order_item.notes == "Updated notes"


def test_order_item_relationships(db_session, fake_order_item, fake_order, fake_product):
    assert fake_order_item.order.id == fake_order.id
    assert fake_order_item.product.id == fake_product.id


def test_delete_order_item(db_session, fake_order_item):
    db_session.delete(fake_order_item)
    db_session.commit()
    deleted_order_item = db_session.query(OrderItemEntity).filter_by(id=fake_order_item.id).first()
    assert deleted_order_item is None


def test_order_item_without_order_id_should_fail(db_session, fake_product):
    item_no_order = OrderItemEntity(
        order_id=None,
        product_id=fake_product.id,
        quantity=1,
        unit_price=Decimal('10.00'),
        subtotal=Decimal('10.00'),
        notes="No order"
    )
    db_session.add(item_no_order)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()

def test_order_item_without_product_id_should_fail(db_session, fake_order):
    item_no_product = OrderItemEntity(
        order_id=fake_order.id,
        product_id=None,
        quantity=1,
        unit_price=Decimal('10.00'),
        subtotal=Decimal('10.00'),
        notes="No product"
    )
    db_session.add(item_no_product)
    with pytest.raises(Exception):
        db_session.commit()

def test_find_order_itens_by_order(db_session, fake_order, fake_order_item):
    order_items = db_session.query(OrderItemEntity).filter_by(order_id=fake_order.id).all()
    assert len(order_items) >= 1
    assert any(item.id == fake_order_item.id for item in order_items)


def test_reverse_relationships(db_session, fake_order, fake_product, fake_order_item):
    assert fake_order_item in fake_order.order_items
    assert fake_order_item in fake_product.order_items
