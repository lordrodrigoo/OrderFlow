import os
import logging
from typing import List, Optional
from fastapi import APIRouter, Response, Query, status, Depends
from src.usecases.review_usecases import ReviewUsecase
from src.dto.request.review_request import ReviewRequest, ReviewFilters
from src.dto.response.review_response import ReviewResponse
from src.dto.response.user_response import UserResponse
from src.api.dependencies import get_review_usecase, get_current_user



API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
REVIEW_PREFIX = f"{API_V1_PREFIX}/reviews"

router = APIRouter(prefix=REVIEW_PREFIX, tags=["reviews"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review_request: ReviewRequest,
    response: Response,
    current_user: UserResponse = Depends(get_current_user),
    review_usecase: ReviewUsecase = Depends(get_review_usecase)
):
    """Endpoint to create a new review."""
    review_request.user_id = current_user.id
    logger.info("Creating review", extra={"product_id": review_request.product_id})
    review = review_usecase.create_review(review_request)
    response.headers['Location'] = f"{REVIEW_PREFIX}/{review.id}"
    return review


@router.get("/{review_id}", response_model=ReviewResponse, status_code=status.HTTP_200_OK)
def get_review_by_id(
    review_id: int,
    response: Response,
    review_usecase: ReviewUsecase = Depends(get_review_usecase)
):
    """Endpoint to get a review by review_id."""
    review = review_usecase.get_review_by_id(review_id)
    response.headers['Location'] = f"{REVIEW_PREFIX}/{review.id}"
    return review


@router.get("/", response_model=List[ReviewResponse], status_code=status.HTTP_200_OK)
def list_reviews(
    product_id: Optional[int] = Query(None, description="Filter reviews by product ID"),
    user_id: Optional[int] = Query(None, description="Filter reviews by user ID"),
    min_rating: Optional[int] = Query(None, description="Filter reviews by minimum rating"),
    max_rating: Optional[int] = Query(None, description="Filter reviews by maximum rating"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Maximum number of records to return"),
    review_usecase: ReviewUsecase = Depends(get_review_usecase)
):
    """Endpoint to list reviews with optional filters."""
    filters = ReviewFilters(
        product_id=product_id,
        user_id=user_id,
        min_rating=min_rating,
        max_rating=max_rating,
        skip=skip,
        limit=limit
    )
    return review_usecase.list_reviews(filters)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: UserResponse = Depends(get_current_user),
    review_usecase: ReviewUsecase = Depends(get_review_usecase)
):
    """Endpoint to delete a review by review_id."""
    review_usecase.delete_review(review_id, current_user.id, current_user.role)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
