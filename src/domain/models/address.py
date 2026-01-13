#pylint: disable=redefined-builtin
from datetime import datetime

class Address:
    def __init__(
        self,
        id: int,
        user_id: int,
        street: str,
        number: str,
        complement: str,
        neighborhood: str,
        city: str,
        state: str,
        zip_code: str,
        is_default: bool,
        created_at: datetime,
        updated_at: datetime = None
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.is_default = is_default
        self.created_at = created_at
        self.updated_at = updated_at
