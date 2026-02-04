# pylint: disable=redefined-builtin
from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from enum import Enum
import bcrypt


class AccountStatus(Enum):
    """Enumeration for account status."""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'

@dataclass
class Account:
    """Entity of domain - it represents an account in the system."""
    user_id: int
    username: str
    password_hash: str
    status: AccountStatus
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def is_active(self) -> bool:
        """Returns the active status of the account."""
        return self.status

    @staticmethod
    def create_account(
        user_id: int,
        username: str,
        password_hash: str,
        status: AccountStatus,
        id: Optional[int] = None,
    ) -> 'Account':
        """Factory method to create a new account instance."""
        return Account(
            id=id,
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            status=status
        )

    @staticmethod
    def from_entity(entity) -> 'Account':
        """Converts an AccountEntity to an Account domain model."""
        return Account(
            id=entity.id,
            user_id=entity.user_id,
            username=entity.username,
            password_hash=entity.password_hash,
            status=AccountStatus(entity.status),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()).decode('utf-8'
        )
