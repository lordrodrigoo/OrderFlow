from typing import List
from decimal import Decimal
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.product import ProductEntity
from src.domain.repositories.product_repository import ProductRepositoryInterface
from src.domain.models.product import Product
from src.infra.db.repositories.base_repository import BaseRepository


class ProductRepository(ProductRepositoryInterface, BaseRepository[ProductEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), ProductEntity)

    def create_product(self, product: Product) -> Product:
        entity = ProductEntity(
            name = product.name,
            description = product.description,
            price = product.price,
            image_url = product.image_url,
            is_available = product.is_available,
            created_at = product.created_at,
            updated_at = product.updated_at
        )
        self.add(entity)
        self.save()
        return Product.from_entity(entity)

    def update_product(self, product: Product) -> Product:
        entity = self.get_by_id(product.id)
        if entity:
            entity.name = product.name
            entity.description = product.description
            entity.price = product.price
            entity.image_url = product.image_url
            entity.is_available = product.is_available
            entity.updated_at = product.updated_at
            self.save()
        return Product.from_entity(entity)

    def get_all_products(self) -> List[Product]:
        return [Product.from_entity(product) for product in self.get_all()]

    def find_products_by_category(self, category_id: int) -> List[Product]:
        entities = self.session.query(self.model).filter(self.model.category_id == category_id).all()
        return [Product.from_entity(product) for product in entities]

    def find_products_by_availability(self, is_available: bool) -> List[Product]:
        entities = self.session.query(self.model).filter(self.model.is_available == is_available).all()
        return [Product.from_entity(product) for product in entities]

    def find_products_by_price_range(self, min_price: Decimal, max_price: Decimal) -> List[Product]:
        entities = self.session.query(self.model).filter(self.model.price.between(min_price, max_price)).all()
        return [Product.from_entity(product) for product in entities]

    def search_products_by_name(self, name):
        entities = self.session.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()
        return [Product.from_entity(product) for product in entities]

    def count_products_by_category(self, category_id: int) -> int:
        count = self.session.query(self.model).filter(self.model.category_id == category_id).count()
        return count

    def delete_product(self, product_id: int) -> bool:
        entity = self.get_by_id(product_id)

        if entity:
            self.delete(entity)
            self.save()
            return True
        return False
