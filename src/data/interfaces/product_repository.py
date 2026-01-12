from abc import ABC, abstractmethod
from typing import List
from decimal import Decimal
from datetime import datetime
from src.domain.models.product import Product

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def insert_product(
        self,
        name: str,
        description: str,
        category_id: int,
        price: Decimal,
        image_url: str,
        is_available: bool,
        preparation_time_minutes: int,
        created_at: datetime,
        updated_at: datetime
    ) -> Product:
        pass

    @abstractmethod
    def select_product(self, name: str) -> List[Product]: pass
