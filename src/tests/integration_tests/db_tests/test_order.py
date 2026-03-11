#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
from decimal import Decimal
import pytest
from src.infra.db.entities.order import OrderEntity


def test_create_order(db_session, fake_order):
    assert fake_order.id is not None
    assert fake_order.user_id == fake_order.user_id
    assert fake_order.total_amount == Decimal('150.75')
    assert fake_order.status == "pending"


def test_order_status(db_session, fake_order):
    fake_order.status = "shipped"
    db_session.commit()
    updated_order = db_session.query(OrderEntity).filter_by(id=fake_order.id).first()
    assert updated_order.status == "shipped"

def test_find_order_by_id(db_session, fake_order):
    found_order = db_session.query(OrderEntity).filter_by(id=fake_order.id).first()
    assert found_order is not None
    assert found_order.id == fake_order.id


def test_find_all_orders(db_session, fake_order):
    orders = db_session.query(OrderEntity).all()
    assert len(orders) >= 1


def test_relationship_between_user_and_order(db_session, fake_user, fake_order):
    # This test I will use fake_order to access the user relationship
    order = db_session.query(OrderEntity).filter_by(id=fake_order.id).first()
    assert order.user.id == fake_order.user_id
    assert order.user.email == fake_order.user.email


def test_order_without_user_should_fail(db_session, fake_address):
    order = OrderEntity(
        user_id=None,
        address_id=fake_address.id,
        total_amount=Decimal('100.00'),
        delivery_fee=Decimal('10.00'),
        status="pending",
        notes="No user",
        scheduled_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(order)
    with pytest.raises(Exception):
        db_session.commit()
