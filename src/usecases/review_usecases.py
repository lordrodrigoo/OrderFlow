from typing import Optional
from src.domain.models.review import Review
from src.dto.request.review_request import ReviewRequest
from src.dto.response.review_response import ReviewResponse
from src.domain.repositories.review_repository import ReviewRepositoryInterface
from src.domain.repositories.user_repository import UserRepositoryInterface
from src.domain.repositories.product_repository import ProductRepositoryInterface
from src.exceptions.exception_handlers_review import (
    ReviewNotFoundException,
    InvalidReviewException
)
from src.exceptions.exception_handlers_user import UserNotFoundException
from src.exceptions.exception_handlers_product import ProductNotFoundException


class ReviewUsecase:
    def __init__(
            self,
            review_repository: ReviewRepositoryInterface,
            user_repository: UserRepositoryInterface,
            product_repository: ProductRepositoryInterface
        ):
        self.review_repository = review_repository
        self.user_repository = user_repository
        self.product_repository = product_repository


    def create_review(self, review_request: ReviewRequest) -> ReviewResponse:
        user = self.user_repository.find_user_by_id(review_request.user_id)

        if not user:
            raise UserNotFoundException(user_id=review_request.user_id)

        product = self.product_repository.find_product_by_id(review_request.product_id)
        if not product:
            raise ProductNotFoundException(product_id=review_request.product_id)

        review_entity = Review(
            user_id=review_request.user_id,
            product_id=review_request.product_id,
            rating=review_request.rating,
            comment=review_request.comment
        )
        created_review = self.review_repository.create_review(review_entity)
        return ReviewResponse(**created_review.__dict__)




    def get_review_by_id(self, review_id: int) -> ReviewResponse:
        review = self.review_repository.get_review_by_id(review_id)
        if not review:
            raise ReviewNotFoundException(review_id=review_id)
        return ReviewResponse(**review.__dict__)


    def list_reviews(
        self,
        product_id: Optional[int] = None,
        user_id: Optional[int] = None,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        skip: int = 0,
        limit: int = 10
) -> list[ReviewResponse]:
        if user_id:
            user = self.user_repository.find_user_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id=user_id)

        if product_id:
            product = self.product_repository.find_product_by_id(product_id)
            if not product:
                raise ProductNotFoundException(product_id=product_id)

        if min_rating and max_rating and min_rating > max_rating:
            raise InvalidReviewException("min_rating cannot be greater than max_rating")

        reviews = self.review_repository.get_all_reviews(
            product_id=product_id,
            user_id=user_id,
            min_rating=min_rating,
            max_rating=max_rating,
            skip=skip,
            limit=limit
        )
        return [ReviewResponse(**review.__dict__) for review in reviews]


    def delete_review(self, review_id: int) -> None:
        review = self.review_repository.get_review_by_id(review_id)
        if not review:
            raise ReviewNotFoundException(review_id=review_id)
        self.review_repository.delete_review(review_id)
