from typing import List
from decimal import Decimal
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.product import Product as ProductEntity
from src.data.interfaces.product_repository import ProductRepositoryInterface
from src.domain.models.product import Product

class ProductRepository(ProductRepositoryInterface):

    @classmethod
    def insert_product(
        cls,
        name: str,
        description: str,
        category_id: int,
        price: Decimal,
        image_url: str,
        is_available: bool,
        preparation_time_minutes: int,
        created_at: str,
        updated_at: str
    ) -> Product:
        with DBConnectionHandler() as db_connection:
            try:
                new_registry = ProductEntity(
                   name = name,
                   description = description,
                   category_id = category_id,
                   price = price,
                   image_url = image_url,
                   is_available = is_available,
                   preparation_time_minutes = preparation_time_minutes,
                   created_at = created_at,
                   updated_at = updated_at
                )
                db_connection.session.add(new_registry)
                db_connection.session.commit()
            except Exception as exception:
                db_connection.session.rollback()
                raise exception

    @classmethod
    def select_product(cls, name: str) -> List[Product]:
        with DBConnectionHandler() as db_connection:
            try:
                products = (
                    db_connection.session
                    .query(ProductEntity)
                    .filter(ProductEntity.name == name)
                    .all()
                )
                return products
            except Exception as exception:
                db_connection.session.rollback()
                raise exception
