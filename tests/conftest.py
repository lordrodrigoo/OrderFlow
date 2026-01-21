#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
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
