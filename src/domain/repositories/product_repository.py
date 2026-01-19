from abc import ABC, abstractmethod
from src.domain.models.product import Product

class ProductRepositoryInterface(ABC):
    """This interface defines the contract for product repository."""

    @abstractmethod
    def create_product(self, product: Product) -> Product: pass

    @abstractmethod
    def update_product(self, product: Product) -> Product: pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool: pass

    @abstractmethod
    def find_products_by_category(self, category_id: int) -> list[Product]: pass

    @abstractmethod
    def find_products_by_availability(self, is_available: bool) -> list[Product]: pass

    @abstractmethod
    def find_products_by_price_range(self, min_price: float, max_price: float) -> list[Product]: pass

    @abstractmethod
    def search_products_by_name(self, name: str) -> list[Product]: pass

    @abstractmethod
    def count_products_by_category(self, category_id: int) -> int: pass

    @abstractmethod
    def get_all_products(self) -> list[Product]: pass
