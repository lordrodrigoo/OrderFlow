from datetime import datetime
from decimal import Decimal
import pytest
from src.infra.db.entities.product import ProductEntity



@pytest.fixture
def fake_product(db_session, fake_category):
    product = ProductEntity(
        name = "Test Product",
        description = "This is a test product",
        price = Decimal('19.99'),
        image_url = "http://example.com/image.png",
        is_available = True,
        preparation_time = 15,
        created_at = datetime.now(),
        updated_at = None,
        category_id = fake_category.id
    )
    db_session.add(product)
    db_session.commit()
    return product


@pytest.fixture
def valid_product_data(fake_category):
    return {
        "name": "New Product",
        "description": "This is a new product",
        "price": float('29.99'),
        "image_url": "http://example.com/new_image.png",
        "is_available": True,
        "preparation_time": 20,
        "category_id": fake_category.id
    }
