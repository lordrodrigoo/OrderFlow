from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from src.infra.db.entities.order import OrderEntity



@pytest.fixture
def fake_order(db_session, fake_user, fake_address):
    order = OrderEntity(
        user_id = fake_user.id,
        address_id = fake_address.id,
        total_amount = Decimal('150.75'),
        delivery_fee = Decimal('5.00'),
        status = "pending",
        notes = "Please deliver between 5-6 PM",
        scheduled_date = datetime.now(),
        created_at = datetime.now(),
        updated_at = None
    )
    db_session.add(order)
    db_session.commit()
    return order


@pytest.fixture
def valid_order_data(fake_address):
    return {
        "address_id": fake_address.id,
        "total_amount": 150.75,
        "delivery_fee": 5.00,
        "notes": "Please deliver between 5-6 PM",
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat()
    }
