from typing import List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.review import ReviewEntity
from src.domain.repositories.review_repository import ReviewRepositoryInterface
from src.domain.models.review import Review
from src.infra.db.repositories.base_repository import BaseRepository


class ReviewRepository(ReviewRepositoryInterface, BaseRepository[ReviewEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.session, ReviewEntity)

    def create_review(self, review: Review) -> Review:
        entity = ReviewEntity(
            rating = review.rating,
            comment = review.comment,
            created_at = review.created_at,
            user_id = review.user_id,
            product_id = review.product_id,
        )
        self.add(entity)
        self.save()
        return Review.from_entity(entity)

    def get_review_by_id(self, review_id: int) -> Review | None:
        entity = self.get_by_id(review_id)
        if entity:
            return Review.from_entity(entity)
        return None

    def find_reviews_by_user(self, user_id: int) -> List[Review]:
        entities = self.session.query(self.model).filter(self.model.user_id == user_id).all()
        return [Review.from_entity(review) for review in entities]

    def find_reviews_by_rating(self, min_rating: int, max_rating: int) -> List[Review]:
        entities = self.session.query(
            self.model).filter(self.model.rating.between(min_rating, max_rating)).all()
        return [Review.from_entity(review) for review in entities]

    def get_all_reviews(self) -> List[Review]:
        return [Review.from_entity(review) for review in self.get_all()]

    def delete_review(self, review_id: int) -> bool:
        return self.delete_by_id(review_id)
