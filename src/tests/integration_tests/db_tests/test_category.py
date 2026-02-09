#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
#pylint: disable=unused-import
import pytest
from src.infra.db.entities.category import CategoryEntity


def test_create_category(db_session, fake_category):
    assert fake_category.id is not None
    assert fake_category.name == "Sample Category"


def test_update_category(db_session, fake_category):
    fake_category.name = "Updated Category"
    db_session.commit()
    updated_category = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert updated_category.name == "Updated Category"


def test_unique_name(db_session, fake_category):
    duplicate_category = CategoryEntity(
        name="Sample Category",  # same name as fake_category
        description="Another category with the same name.",
    )
    db_session.add(duplicate_category)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()


def test_delete_category(db_session, fake_category):
    db_session.delete(fake_category)
    db_session.commit()
    deleted_category = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert deleted_category is None


def test_relationships_between_category_and_products(db_session, fake_category):
    # This test will check if the relationship between CategoryEntity and ProductEntity works
    category = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert category.products == []  # Initially, there should be no products associated
