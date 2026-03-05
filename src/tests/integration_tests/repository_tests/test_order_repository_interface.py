from datetime import datetime
from decimal import Decimal
from src.domain.models.order import Order, OrderStatus
from src.infra.db.repositories.order_repository_interface import OrderRepository
from src.tests.helpers import FakeDBConnectionHandler





def test_create_order(db_session,fake_user, fake_address):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    order = Order(
        user_id=fake_user.id,
        address_id=fake_address.id,
        status=OrderStatus.PENDING,
        total_amount=Decimal('150.75'),
        delivery_fee=Decimal('5.00'),
        notes="Please deliver between 5-6 PM",
        scheduled_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=None
    )
    created_order = order_repo.create_order(order)
    assert created_order.id is not None
    assert created_order.user_id == fake_user.id
    assert created_order.status == OrderStatus.PENDING
    assert created_order.total_amount == Decimal('150.75')
    assert created_order.delivery_fee == Decimal('5.00')


def test_update_order(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    order = Order(
        id=fake_order.id,
        user_id=fake_order.user_id,
        address_id=fake_order.address_id,
        status=OrderStatus.PAID,
        total_amount=Decimal('160.00'),
        delivery_fee=fake_order.delivery_fee,
        notes=fake_order.notes,
        scheduled_date=fake_order.scheduled_date,
        created_at=fake_order.created_at,
        updated_at=datetime.now()
    )
    updated_order = order_repo.update_order(order)

    assert updated_order.status == OrderStatus.PAID
    assert updated_order.total_amount == Decimal('160.00')


def test_update_order_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)
    order = Order(id=9999, user_id=1, address_id=1, status=OrderStatus.PAID, total_amount=10, delivery_fee=1)
    result = order_repo.update_order(order)
    assert result is None or result.id is None



def test_get_all_orders(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    orders = order_repo.get_all_orders()
    assert len(orders) > 0
    assert any(order.id == fake_order.id for order in orders)


def test_get_order_by_id(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    order = order_repo.get_order_by_id(fake_order.id)
    assert order is not None
    assert order.id == fake_order.id
    assert order.user_id == fake_order.user_id
    assert order.status == OrderStatus.PENDING
    assert order.total_amount == Decimal('150.75')
    assert order.delivery_fee == Decimal('5.00')


def test_get_order_by_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)
    result = order_repo.get_order_by_id(9999)
    assert result is None


def test_find_orders_by_total_amount(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    orders = order_repo.find_orders_by_total_amount(Decimal('100.00'), Decimal('200.00'))
    assert len(orders) > 0
    assert any(order.id == fake_order.id for order in orders)


def test_cancel_order(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    result = order_repo.cancel_order(fake_order.id)
    assert result is True

    canceled_order = order_repo.get_order_by_id(fake_order.id)
    assert canceled_order.status == OrderStatus.CANCELED


def test_cancel_order_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)
    result = order_repo.cancel_order(9999)
    assert result is False


def test_delete_order(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    order_repo.delete_order(fake_order.id)
    deleted_order = order_repo.get_order_by_id(fake_order.id)
    assert deleted_order is None



def test_exists(db_session, fake_order):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)

    assert order_repo.exists(fake_order.id) is True
    assert order_repo.exists(9999) is False



def test_delete_order_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)
    result = order_repo.delete_order(9999)
    assert result is False

def test_exists_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    order_repo = OrderRepository(db_handler)
    result = order_repo.exists(9999)
    assert result is False
