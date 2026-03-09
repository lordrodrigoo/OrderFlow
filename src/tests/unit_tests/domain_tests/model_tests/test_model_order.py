# pylint: disable=redefined-outer-name
from types import SimpleNamespace
from datetime import datetime, timedelta
import pytest
from src.domain.models.order import Order, OrderStatus
from src.infra.db.entities.order import OrderEntity


@pytest.fixture
def order_data():
    now = datetime.now()
    return {
        "id": 1,
        "user_id": 1,
        "address_id": 2,
        "total_amount": 150.0,
        "delivery_fee": 10.0,
        "notes": "Please deliver between 6-7 PM",
        "scheduled_date": None,
        "status": OrderStatus.PENDING,
        "created_at": now,
        "updated_at": now
    }

def test_create_order():
    order = Order.create_order(
        user_id=1,
        address_id=2,
        total_amount=150.0,
        delivery_fee=10.0,
        notes="Please deliver between 6-7 PM",
        scheduled_date="2026-03-05 19:00:00",
        status=OrderStatus.PENDING
    )
    assert isinstance(order, Order)
    assert order.user_id == 1
    assert order.address_id == 2
    assert order.total_amount == 150.0
    assert order.delivery_fee == 10.0
    assert order.notes == "Please deliver between 6-7 PM"
    assert order.scheduled_date == "2026-03-05 19:00:00"
    assert order.status == OrderStatus.PENDING


def test_from_entity(order_data):
    entity = SimpleNamespace(**order_data)
    order = Order.from_entity(entity)
    for key in order_data:
        assert getattr(order, key) == order_data[key]


def test_scheduled_info_property_with_date(order_data):
    scheduled_date = datetime.now() + timedelta(days=1)
    order_data["scheduled_date"] = scheduled_date
    order = Order(**order_data)
    expected_info = f"Scheduled for {scheduled_date.strftime('%Y-%m-%d %H:%M:%S')}"
    assert order.scheduled_info == expected_info


def test_scheduled_info_property_without_date(order_data):
    order_data["scheduled_date"] = None
    order = Order(**order_data)
    assert order.scheduled_info == "No scheduled date"



def test_is_delivered_property(order_data):
    order_data["status"] = OrderStatus.DELIVERED
    order = Order(**order_data)
    assert order.is_delivered is True


def test_is_pending_property(order_data):
    order_data["status"] = OrderStatus.PENDING
    order = Order(**order_data)
    assert order.is_pending is True


def test_summary_property(order_data):
    order = Order(**order_data)
    expected_summary = "Order 1: pending - Total: $150.00"
    assert order.summary == expected_summary

def test_is_paid_property(order_data):
    order_data["status"] = OrderStatus.PAID
    order = Order(**order_data)
    assert order.is_paid is True


def test_repr():
    order = OrderEntity(
        id = 1,
        user_id = 1,
        total_amount = 150.0,
        status = OrderStatus.PENDING
    )
    expected = "Order [id = 1, user_id = 1, total_amount = 150.0, status = OrderStatus.PENDING]"
    assert repr(order) == expected
