from abc import ABC, abstractmethod
from src.domain.models.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

    @abstractmethod
    def list_products(self) -> list[Product]:
        pass
