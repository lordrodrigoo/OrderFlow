from abc import ABC, abstractmethod
from src.domain.models.review import Review

class ReviewRepository(ABC):
    @abstractmethod
    def add_review(self, review: Review) -> None:
        pass

    @abstractmethod
    def get_review_by_id(self, review_id: int) -> Review:
        pass

    @abstractmethod
    def update_review(self, review: Review) -> None:
        pass

    @abstractmethod
    def delete_review(self, review_id: int) -> None:
        pass

    @abstractmethod
    def list_reviews(self) -> list[Review]:
        pass
