#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
from src.infra.db.entities.review import ReviewEntity


def test_create_review(db_session, fake_review):
    assert fake_review.id is not None
    assert fake_review.rating == 5
    assert fake_review.comment == "Great product!"


def test_update_review(db_session, fake_review):
    fake_review.rating = 4
    fake_review.comment = "Good but could be better."
    db_session.commit()
    updated_review = db_session.query(ReviewEntity).filter_by(id=fake_review.id).first()
    assert updated_review.rating == 4
    assert updated_review.comment == "Good but could be better."



def test_relationship_between_product_and_review(db_session, fake_product, fake_review):
    # This test I will use fake_review to access the product relationship
    review = db_session.query(ReviewEntity).filter_by(id=fake_review.id).first()
    assert review.product.id == fake_review.product_id
    assert review.product.name == fake_product.name
    assert review.user_id == fake_review.user_id


def test_relationship_between_user_and_review(db_session, fake_user, fake_review):
    # This test I will use fake_review to access the user relationship
    review = db_session.query(ReviewEntity).filter_by(id=fake_review.id).first()
    assert review.user.id == fake_review.user_id
    assert review.user.email == fake_user.email
    assert review.product_id == fake_review.product_id


def test_relationship_between_order_and_review(db_session, fake_order, fake_review):
    # This test I will use fake_review to access the order relationship
    review = db_session.query(ReviewEntity).filter_by(id=fake_review.id).first()
    assert review.order.id == fake_review.order_id
    assert review.order.total_amount == fake_order.total_amount
    assert review.user_id == fake_review.user_id


def test_delete_review(db_session, fake_review):
    db_session.delete(fake_review)
    db_session.commit()
    deleted_review = db_session.query(ReviewEntity).filter_by(id=fake_review.id).first()
    assert deleted_review is None
