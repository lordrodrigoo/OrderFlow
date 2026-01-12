from decimal import Decimal
import pytest
from sqlalchemy import text
from src.infra.db.repositories.product_repository import ProductRepository
from src.infra.db.settings.connection import DBConnectionHandler


db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()

@pytest.mark.skip(reason="Sensible to database state")
def test_insert_product_with_category():
    # Create a category to associate with the product
    category_name = "Test Category"
    category_description = "This is a test category."
    insert_category_sql = f"""
        INSERT INTO categories (name, description)
        VALUES ('{category_name}', '{category_description}')
    """
    category_response = connection.execute(text(insert_category_sql))
    connection.commit()
    category_id = category_response.fetchone()[0]

    # Product data
    mocked_name = "Test Product"
    mocked_description = "This is a test product."
    mocked_price = Decimal('19.99')
    mocked_image_url = "http://example.com/image.jpg"
    mocked_is_available = True
    mocked_preparation_time_minutes = 15
    mocked_created_at = "2024-01-01T12:00:00"
    mocked_updated_at = "2024-01-01T12:00:00"

    product_repository = ProductRepository()
    product_repository.insert_product(
        name=mocked_name,
        description=mocked_description,
        category_id=category_id,
        price=mocked_price,
        image_url=mocked_image_url,
        is_available=mocked_is_available,
        preparation_time_minutes=mocked_preparation_time_minutes,
        created_at=mocked_created_at,
        updated_at=mocked_updated_at
    )

    sql = f"""
        SELECT * FROM products
        WHERE name = '{mocked_name}'
        AND description = '{mocked_description}'
        AND price = {mocked_price}
        AND category_id = {category_id}
    """
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.name == mocked_name
    assert registry.description == mocked_description
    assert registry.price == mocked_price

    # Delete category and product after test
    product_id = registry[0]
    connection.execute(text(f'''
        DELETE FROM products WHERE id = '{product_id}'
    '''))
    connection.execute(text(f'''
        DELETE FROM categories WHERE id = '{category_id}'
    '''))
    connection.commit()
