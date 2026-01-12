
from sqlalchemy import text
from sqlalchemy import Numeric
from src.infra.db.repositories.product_repository import ProductRepository
from src.infra.db.settings.connection import DBConnectionHandler


db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


def test_insert_product_with_category():
    # Cria uma categoria
    category_name = "Test Category"
    category_description = "This is a test category."
    insert_category_sql = f"""
        INSERT INTO categories (name, description)
        VALUES ('{category_name}', '{category_description}')
        RETURNING id
    """
    category_response = connection.execute(text(insert_category_sql))
    connection.commit()
    category_id = category_response.fetchone()[0]

    # Dados do produto
    mocked_name = "Test Product"
    mocked_description = "This is a test product."
    mocked_price = 19.99
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
    """
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.name == mocked_name
    assert registry.description == mocked_description
    assert Numeric(registry.price) == mocked_price

    # connection.execute(text(f'''
    #     DELETE FROM products WHERE id = '{registry.id}'
    # '''))
    # connection.commit()
