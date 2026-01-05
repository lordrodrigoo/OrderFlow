#pylint: disable=redefined-builtin
from datetime import datetime

class Review:
    def __init__(
        self,
        id: int,
        user_id: int,
        rating: int,
        comment: str,
        created_at: datetime
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at
