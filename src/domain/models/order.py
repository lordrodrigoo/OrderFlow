from decimal import Decimal
from datetime import datetime


class Orders:
    def __init__(
        self,
        user_id: int,
        address_id: int,
        adress_id: int,
        status: str,
        total_amount: Decimal,
        delivery_fee: Decimal,
        notes: str,
        scheduled_date: datetime,
        created_at: datetime,
        updated_at: datetime
    ) -> None:
        self.user_id = user_id
        self.address_id = address_id
        self.adress_id = adress_id
        self.status = status
        self.total_amount = total_amount
        self.delivery_fee = delivery_fee
        self.notes = notes
        self.scheduled_date = scheduled_date
        self.created_at = created_at
        self.updated_at = updated_at
