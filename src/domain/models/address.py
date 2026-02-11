from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    """Entity od domain - it represents an address in the system."""
    user_id: int
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str
    is_default: bool
    id: Optional[int] = None
    complement: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_address(self) -> str:
        """Returns the full address as a formatted string."""
        complement_str = f", {self.complement}" if self.complement else ""
        return f"{self.street}, {self.number}{complement_str}, {self.city}, {self.state}, {self.zip_code}"

    @staticmethod
    def create_address(
        user_id: int,
        street: str,
        number: str,
        city: str,
        state: str,
        zip_code: str,
        is_default: bool,
        neighborhood: str,
        complement: Optional[str] = None

    ) -> 'Address':
        """Factory method to create a new address instance."""
        return Address(
            user_id=user_id,
            street=street,
            number=number,
            complement=complement,
            city=city,
            neighborhood=neighborhood,
            state=state,
            zip_code=zip_code,
            is_default=is_default
        )

    @staticmethod
    def from_entity(entity) -> 'Address':
        """Converts an AddressEntity to an Address domain model."""
        return Address(
            id=entity.id,
            user_id=entity.user_id,
            street=entity.street,
            number=entity.number,
            complement=entity.complement,
            neighborhood=entity.neighborhood,
            city=entity.city,
            state=entity.state,
            zip_code=entity.zip_code,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
