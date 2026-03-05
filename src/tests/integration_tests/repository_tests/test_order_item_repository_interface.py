from src.domain.models.order_item import OrderItem
from src.infra.db.repositories.order_item_repository_interface import OrderItemRepository
from src.tests.helpers import FakeDBConnectionHandler



def test_create_order_item(db_session, fake_order, fake_product):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    order_item = OrderItem(
        order_id=fake_order.id,
        product_id=fake_product.id,
        quantity=2,
        unit_price=fake_product.price,
        subtotal=fake_product.price * 2,
        notes="Handle with care"
    )
    created_order_item = order_item_repo.create_order_item(order_item)
    assert created_order_item.id is not None
    assert created_order_item.order_id == fake_order.id
    assert created_order_item.product_id == fake_product.id
    assert created_order_item.quantity == 2
    assert created_order_item.unit_price == fake_product.price
    assert created_order_item.subtotal == fake_product.price * 2
    assert created_order_item.notes == "Handle with care"


def test_update_order_item(db_session, fake_order_item):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    order_item = OrderItem(
        id=fake_order_item.id,
        order_id=fake_order_item.order_id,
        product_id=fake_order_item.product_id,
        quantity=3,
        unit_price=fake_order_item.unit_price,
        subtotal=fake_order_item.unit_price * 3,
        notes="Handle with care - updated"
    )
    updated_order_item = order_item_repo.update_order_item(order_item)

    assert updated_order_item.quantity == 3
    assert updated_order_item.subtotal == fake_order_item.unit_price * 3
    assert updated_order_item.notes == "Handle with care - updated"


def test_get_all_order_items(db_session, fake_order_item):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    order_items = order_item_repo.get_all_order_items()
    assert len(order_items) > 0
    assert any(item.id == fake_order_item.id for item in order_items)


def test_delete_order_item(db_session, fake_order_item):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    order_item_repo.delete_order_item(fake_order_item.id)
    deleted_item = order_item_repo.get_order_item_by_id(fake_order_item.id)
    assert deleted_item is None


def test_get_order_item_by_id(db_session, fake_order_item):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    order_item = order_item_repo.get_order_item_by_id(fake_order_item.id)
    assert order_item is not None
    assert order_item.id == fake_order_item.id
    assert order_item.order_id == fake_order_item.order_id
    assert order_item.product_id == fake_order_item.product_id
    assert order_item.quantity == fake_order_item.quantity
    assert order_item.unit_price == fake_order_item.unit_price
    assert order_item.subtotal == fake_order_item.subtotal
    assert order_item.notes == fake_order_item.notes


def test_exists(db_session, fake_order, fake_product, fake_order_item):
    db_handler = FakeDBConnectionHandler(db_session)
    order_item_repo = OrderItemRepository(db_handler)

    exists = order_item_repo.exists(order_id=fake_order.id, product_id=fake_product.id)
    assert exists is True

    non_existent_id = fake_order_item.id + 999
    exists = order_item_repo.exists(order_id=non_existent_id, product_id=fake_product.id)
    assert exists is False
