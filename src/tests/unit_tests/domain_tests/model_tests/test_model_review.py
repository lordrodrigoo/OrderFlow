from src.domain.models.review import Review
from src.infra.db.entities.review import ReviewEntity


def test_create_review():
    review = Review.create_review(
        user_id=1,
        product_id=2,
        rating=5,
        comment="Excellent product!"
    )
    assert isinstance(review, Review)
    assert review.user_id == 1
    assert review.product_id == 2
    assert review.rating == 5
    assert review.comment == "Excellent product!"


def test_from_entity():
    class MockReviewEntity:
        def __init__(self):
            self.id = 1
            self.user_id = 1
            self.product_id = 2
            self.rating = 5
            self.comment = "Excellent product!"
            self.created_at = None
            self.updated_at = None

    entity = MockReviewEntity()
    review = Review.from_entity(entity)
    assert review.id == 1
    assert review.user_id == 1
    assert review.product_id == 2
    assert review.rating == 5
    assert review.comment == "Excellent product!"
    assert review.created_at is None


def test_is_positive_property():
    review = Review(rating=5)
    assert review.is_positive is True
    review = Review(rating=4)
    assert review.is_positive is True
    review = Review(rating=3)
    assert review.is_positive is False

def test_is_negative_property():
    review = Review(rating=3)
    assert review.is_negative is True
    review = Review(rating=2)
    assert review.is_negative is True
    review = Review(rating=4)
    assert review.is_negative is False


def test_review_repr():
    review = ReviewEntity(id=1, rating=5)
    expected = "Review [id = 1, rating = 5]"
    assert repr(review) == expected
