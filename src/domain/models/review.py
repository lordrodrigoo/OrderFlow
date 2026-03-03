from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Review:
    """Entity of domain - it represents a review in the system."""
    rating: int
    id: Optional[int] = None
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    comment: Optional[str] = None
    created_at: Optional[datetime] = None

    @property
    def is_positive(self) -> bool:
        """Check if the review is positive (rating 4 or 5)."""
        return self.rating >= 4

    @property
    def is_negative(self) -> bool:
        """Check if the review is negative (rating 1 to 3)."""
        return self.rating <= 3

    @staticmethod
    def create_review(
        rating: int,
        user_id: int,
        product_id: int,
        comment: Optional[str] = None
    ) -> 'Review':
        """Factory method to create a new Review."""
        return Review(
            user_id=user_id,
            product_id=product_id,
            rating=rating,
            comment=comment,
            created_at=datetime.now()
        )

    @staticmethod
    def from_entity(entity) -> 'Review':
        """Converts a ReviewEntity to a Review domain model."""
        return Review(
            id=entity.id,
            user_id=entity.user_id,
            product_id=entity.product_id,
            rating=entity.rating,
            comment=entity.comment,
            created_at=entity.created_at
        )
