#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
from decimal import Decimal
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base
from src.infra.db.entities.user import UserEntity
from src.infra.db.entities.account import AccountEntity
from src.infra.db.entities.address import AddressEntity
from src.infra.db.entities.category import CategoryEntity
from src.infra.db.entities.product import ProductEntity
from src.infra.db.entities.order import OrderEntity
from src.infra.db.entities.order_item import OrderItemEntity
from src.infra.db.entities.review import ReviewEntity


@pytest.fixture(scope="function")
def db_session():
    with PostgresContainer("postgres:16") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        session_instance = sessionmaker(bind=engine)
        session = session_instance()
        yield session
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def fake_user(db_session):
    user = UserEntity(
        first_name="Ana",
        last_name="Silva",
        age=28,
        email="ana.silva@example.com",
        phone="123456789",
        is_active=True,
        role="user",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def fake_account(db_session, fake_user):
    account = AccountEntity(
        user_id=fake_user.id,
        username="ana_silva",
        password_hash="StrongHashedPassword123!",
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(account)
    db_session.commit()
    return account


@pytest.fixture
def fake_product(db_session, fake_category):
    product = ProductEntity(
        name = "Test Product",
        description = "This is a test product",
        price = Decimal('19.99'),
        image_url = "http://example.com/image.png",
        is_available = True,
        preparation_time_minutes = 15,
        created_at = datetime.now(),
        updated_at = None,
        category_id = fake_category.id
    )
    db_session.add(product)
    db_session.commit()
    return product


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
def fake_category(db_session):
    category = CategoryEntity(
        name="Sample Category",
        description="This is a sample category for testing.",
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def fake_address(db_session, fake_user):
    address = AddressEntity(
        user_id=fake_user.id,
        street="Main St",
        number="123",
        complement="Apt 4",
        neighborhood="Downtown",
        city="Metropolis",
        state="NY",
        zip_code="12345",
        is_default=True,
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(address)
    db_session.commit()
    return address


@pytest.fixture
def fake_review(db_session, fake_user, fake_order, fake_account, fake_product, fake_category):
    review = ReviewEntity(
        order_id=fake_order.id,
        user_id=fake_user.id,
        product_id=fake_product.id,
        rating=5,
        comment="Great product!",
        created_at=datetime.now()
    )
    db_session.add(review)
    db_session.commit()
    return review
