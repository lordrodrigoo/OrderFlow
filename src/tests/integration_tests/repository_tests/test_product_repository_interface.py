from decimal import Decimal
from src.domain.models.product import Product
from src.infra.db.repositories.product_repository_interface import ProductRepository
from src.tests.helpers import FakeDBConnectionHandler


def test_update_product(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    product = Product.from_entity(fake_product)
    product.name = "Updated Test Product"
    product.description = "This is an updated test product"
    product.price = Decimal('29.99')
    product.image_url = "http://example.com/updated_image.png"
    product.is_available = False
    product.preparation_time = 20

    updated_product = product_repo.update_product(product)
    assert updated_product.name == "Updated Test Product"
    assert updated_product.description == "This is an updated test product"
    assert updated_product.price == Decimal('29.99')
    assert updated_product.image_url == "http://example.com/updated_image.png"
    assert updated_product.is_available is False
    assert updated_product.preparation_time == 20


def test_create_product(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    new_product = Product.create_product(
        name="New Test Product",
        description="This is a new test product",
        price=Decimal('9.99'),
        image_url="http://example.com/new_image.png",
        is_available=True,
        preparation_time=10,
        category_id=fake_category.id
    )
    created_product = product_repo.create_product(new_product)
    assert fake_category.id is not None
    assert created_product.name == "New Test Product"
    assert created_product.description == "This is a new test product"
    assert created_product.price == Decimal('9.99')
    assert created_product.image_url == "http://example.com/new_image.png"
    assert created_product.is_available is True
    assert created_product.preparation_time == 10


def test_get_all_products(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    products = product_repo.get_all_products()
    assert len(products) == 1
    assert products[0].id == fake_product.id


def test_find_products_by_category(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    products = product_repo.find_products_by_category(fake_product.category_id)
    assert len(products) == 1
    assert products[0].id == fake_product.id


def test_find_products_by_availability(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    products = product_repo.find_products_by_availability(fake_product.is_available)
    assert len(products) == 1
    assert products[0].id == fake_product.id


def test_find_products_by_id(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    product = product_repo.find_product_by_id(fake_product.id)
    assert product is not None
    assert product.id == fake_product.id


def test_count_products_by_category(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    count = product_repo.count_products_by_category(fake_product.category_id)
    assert count == 1


def test_find_products_by_name(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    products = product_repo.find_products_by_name("Test Product")
    assert len(products) == 1
    assert products[0].id == fake_product.id


def test_delete_product(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    product_repo = ProductRepository(db_handler)

    product_repo.delete_product(fake_product.id)
    deleted_product = product_repo.find_product_by_id(fake_product.id)
    assert deleted_product is None
