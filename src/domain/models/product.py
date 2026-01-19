from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """Entity of domain - it represents a product in the system."""
    name: str
    description: str
    category_id: int
    price: float
    is_available: bool
    preparation_time: int  # in minutes
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_description(self) -> str:
        """Returns the full description of the product."""
        return f"{self.name}: {self.description}"

    @staticmethod
    def create_product(
        name: str,
        description: str,
        category_id: int,
        price: float,
        is_available: bool,
        preparation_time: int
    ) -> 'Product':
        """Factory method to create a new product instance."""
        return Product(
            name=name,
            description=description,
            category_id=category_id,
            price=price,
            is_available=is_available,
            preparation_time=preparation_time
        )

    @staticmethod
    def from_entity(entity) -> 'Product':
        """Converts a ProductEntity to a Product domain model."""
        return Product(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            category_id=entity.category_id,
            price=entity.price,
            is_available=entity.is_available,
            preparation_time=entity.preparation_time,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
