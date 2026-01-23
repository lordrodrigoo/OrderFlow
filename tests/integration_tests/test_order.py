#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
import pytest
from src.infra.db.entities.order import OrderEntity
from tests.integration_tests.test_user import fake_user
from tests.integration_tests.test_account import fake_account
from tests.integration_tests.test_address import fake_address


@pytest.fixture
def fake_order(db_session, fake_user, fake_account, fake_address):
    order = OrderEntity(
        user_id = fake_user.id,
        total_amount = 150.75,
        status = "pending",
        created_at = datetime.now(),
        updated_at = None
    )
    db_session.add(order)
    db_session.commit()
    return order


def test_create_order(db_session, fake_order):
    assert fake_order.id is not None
    assert fake_order.user_id == fake_order.user_id
    assert fake_order.total_amount == 150.75
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


def test_order_without_user_should_fail(db_session):
    """This test checks that creating an order without a valid user_id fails.
    I will to create an order with a non-existent user_id and expect an exception.
    """
    invalid_order = OrderEntity(
        user_id = 99999,  # assuming this user_id does not exist
        total_amount = 200.00,
        status = "pending",
        created_at = datetime.now(),
        updated_at = None
    )
    db_session.add(invalid_order)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()
