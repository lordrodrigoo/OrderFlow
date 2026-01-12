#pylint: disable=redefined-builtin
from datetime import datetime
from decimal import Decimal

class Product:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        category_id: int,
        price: Decimal,
        image_url: str,
        is_available: bool,
        preparation_time_minutes: int,
        created_at: datetime,
        updated_at: datetime
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.category_id = category_id
        self.price = price
        self.image_url = image_url
        self.is_available = is_available
        self.preparation_time_minutes = preparation_time_minutes
        self.created_at = created_at
        self.updated_at = updated_at
