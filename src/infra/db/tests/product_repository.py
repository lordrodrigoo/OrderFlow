from typing import List
from src.domain.models.product import Product

class ProductRepositorySpy:
    def __init__(self) -> None:
        self.insert_product_attributes = {}
        self.select_product_attributes = {}

    def insert_product(
        self,
        name: str,
        description: str,
        category_id: int,
        price: float,
        image_url: str,
        is_available: bool,
        preparation_time_minutes: int,
        created_at: str,
        updated_at: str
    ) -> Product:
        self.insert_product_attributes["name"] = name
        self.insert_product_attributes["description"] = description
        self.insert_product_attributes["category_id"] = category_id
        self.insert_product_attributes["price"] = price
        self.insert_product_attributes["image_url"] = image_url
        self.insert_product_attributes["is_available"] = is_available
        self.insert_product_attributes["preparation_time_minutes"] = preparation_time_minutes
        self.insert_product_attributes["created_at"] = created_at
        self.insert_product_attributes["updated_at"] = updated_at

    def select_product(self, name: str) -> List[Product]:
        self.select_product_attributes["name"] = name
        return [
            Product(
                id=1,
                name="Pizza Margherita",
                description="Classic pizza with tomatoes, mozzarella cheese, fresh basil, salt, and extra-virgin olive oil.",
                category_id=2,
                price=9.99,
                image_url="http://example.com/pizza.jpg",
                is_available=True,
                preparation_time_minutes=15,
                created_at="2024-01-01T00:00:00",
                updated_at=None
            )
        ]
