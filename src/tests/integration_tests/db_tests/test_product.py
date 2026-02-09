#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from datetime import datetime
from decimal import Decimal
import pytest
from src.infra.db.entities.product import ProductEntity


def test_create_product(db_session, fake_product):
    assert fake_product.id is not None
    assert fake_product.name == "Test Product"
    assert fake_product.price == Decimal('19.99')
    assert fake_product.is_available is True


def test_update_product(db_session, fake_product):
    fake_product.price = Decimal('24.99')
    db_session.commit()
    updated_product = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert updated_product.price == Decimal('24.99')

def test_relationship_between_product_and_category(db_session, fake_product, fake_category):
    product = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert product.category.id == fake_category.id


def test_delete_product(db_session, fake_product):
    db_session.delete(fake_product)
    db_session.commit()
    deleted_product = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert deleted_product is None


def test_find_product_by_id(db_session, fake_product):
    found_product = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert found_product is not None
    assert found_product.id == fake_product.id


def test_find_all_products(db_session, fake_product):
    products = db_session.query(ProductEntity).all()
    assert len(products) >= 1


def test_product_without_category_should_fail(db_session):
    """This test checks that creating a product without a valid category_id fails.
    I will to create a product with a non-existent category_id and expect an exception.
    """
    invalid_product = ProductEntity(
        name = "Invalid Product",
        description = "This product has an invalid category",
        price = Decimal('9.99'),
        image_url = "http://example.com/invalid_image.png",
        is_available = True,
        preparation_time_minutes = 10,
        created_at = datetime.now(),
        updated_at = None,
        category_id = 9999  # assuming this ID does not exist
    )
    db_session.add(invalid_product)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()


def test_unique_name(db_session, fake_category, fake_product):
    """This test checks that the name field in ProductEntity is unique.
    I will create two products with the same name and expect an exception on the second insert.
    """
    duplicate_product = ProductEntity(
        name = "Test Product",  # same name as fake_product
        description = "This is a duplicate test product",
        price = Decimal('29.99'),
        image_url = "http://example.com/duplicate_image.png",
        is_available = True,
        preparation_time_minutes = 20,
        created_at = datetime.now(),
        updated_at = None,
        category_id = fake_category.id
    )
    db_session.add(duplicate_product)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()


def test_relationship_between_product_and_order_items(db_session, fake_product):
    # This test will check if the relationship between ProductEntity and OrderItemEntity is set up correctly.
    product = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert hasattr(product, 'order_items')
    assert isinstance(product.order_items, list)
