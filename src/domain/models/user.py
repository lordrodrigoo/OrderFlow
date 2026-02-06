from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


@dataclass
class Users:
    """Entity of domain - it represents a user in the system."""
    first_name: str
    last_name: str
    age: int
    phone: str
    email: str
    is_active: bool
    id : Optional[int] = None
    role: UserRole = UserRole.USER  #Default role is USER
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create_user(
        first_name: str,
        last_name: str,
        age: int,
        phone: str,
        email: str,
        is_active: bool,
        role: UserRole = UserRole.USER
    ) -> 'Users':
        """Factory method to create a new user instance."""
        return Users(
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone,
            email=email,
            is_active=is_active,
            role=role
        )
    @staticmethod
    def from_entity(entity) -> 'Users':
        """Converts a UserEntity to a Users domain model."""
        return Users(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            age=entity.age,
            phone=entity.phone,
            email=entity.email,
            is_active=entity.is_active,
            role=UserRole(entity.role),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
