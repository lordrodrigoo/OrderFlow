#pylint: disable=redefined-builtin
#pylint: disable=invalid-name
from datetime import datetime


class Users:
    def __init__(self,
        id: int,
        first_name: str,
        last_name: str,
        password_hash: str,
        age: int,
        phone: str,
        email: str,
        is_active: bool,
        created_at: datetime,
        updated_at: datetime
    ) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.age = age
        self.phone = phone
        self.email = email
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
