from src.infra.db.repositories.review_repository_interface import ReviewRepository
from src.tests.helpers import FakeDBConnectionHandler


def test_create_review(fake_review, db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)

    created_review = review_repo.create_review(fake_review)

    assert created_review.id is not None
    assert created_review.rating == fake_review.rating
    assert created_review.comment == fake_review.comment
    assert created_review.user_id == fake_review.user_id
    assert created_review.product_id == fake_review.product_id


def test_get_review_by_id(fake_review, db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)

    created_review = review_repo.create_review(fake_review)
    retrieved_review = review_repo.get_review_by_id(created_review.id)

    assert retrieved_review is not None
    assert retrieved_review.id == created_review.id
    assert retrieved_review.rating == created_review.rating
    assert retrieved_review.comment == created_review.comment
    assert retrieved_review.user_id == created_review.user_id
    assert retrieved_review.product_id == created_review.product_id


def test_get_all_reviews(fake_review, db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)

    review_repo.create_review(fake_review)
    all_reviews = review_repo.get_all_reviews()

    assert any(r.id == fake_review.id for r in all_reviews)


def test_find_reviews_by_rating(fake_review, db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)

    review_repo.create_review(fake_review)
    reviews_by_rating = review_repo.find_reviews_by_rating(3, 5)

    assert any(r.id == fake_review.id for r in reviews_by_rating)


def test_delete_review(fake_review, db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)

    created_review = review_repo.create_review(fake_review)
    review_repo.delete_review(created_review.id)
    deleted_review = review_repo.get_review_by_id(created_review.id)

    assert deleted_review is None


def test_find_reviews_by_user_found(db_session, fake_review):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)
    created_review = review_repo.create_review(fake_review)
    reviews = review_repo.find_reviews_by_user(fake_review.user_id)
    assert any(r.id == created_review.id for r in reviews)


def test_find_reviews_by_user_not_found(db_session):
    db_connection = FakeDBConnectionHandler(db_session)
    review_repo = ReviewRepository(db_connection)
    reviews = review_repo.find_reviews_by_user(9999)
    assert len(reviews) == 0
