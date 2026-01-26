#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
from decimal import Decimal
import pytest
from src.infra.db.entities.product import ProductEntity
from tests.integration_tests.test_category import fake_category



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


def test_create_product(db_session, fake_product):
    assert fake_product.id is not None
    assert fake_product.name == "Test Product"
    assert fake_product.price == Decimal('19.99')
    assert fake_product.is_available is True
