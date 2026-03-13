#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.main import app
from src.api.dependencies import get_db
from src.infra.db.settings.base import Base
from src.infra.db.entities.review import ReviewEntity
from src.tests.helpers import FakeDBConnectionHandler


@pytest.fixture
def client(db_session):
    fake_db = FakeDBConnectionHandler(db_session)
    app.dependency_overrides[get_db] = lambda: fake_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()



@pytest.fixture(scope="session")
def db_engine():
    with PostgresContainer("postgres:16") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)



@pytest.fixture(scope="function")
def db_session(db_engine):
    with db_engine.connect() as connection:
        transaction = connection.begin()
        session = Session(connection)
        try:
            yield session
        finally:
            if transaction.is_active:
                transaction.rollback()


@pytest.fixture
def fake_review(db_session, fake_user, fake_account, fake_product, fake_category):
    review = ReviewEntity(
        user_id=fake_user.id,
        product_id=fake_product.id,
        rating=5,
        comment="Great product!",
        created_at=datetime.now()
    )
    db_session.add(review)
    db_session.commit()
    return review
