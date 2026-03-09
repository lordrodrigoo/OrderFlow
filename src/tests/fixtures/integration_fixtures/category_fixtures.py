import pytest
from src.infra.db.entities.category import CategoryEntity



@pytest.fixture
def fake_category(db_session):
    category = CategoryEntity(
        name="Sample Category",
        description="This is a sample category for testing.",
    )
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def valid_category_data():
    return {
        "name": "New Category",
        "description": "This is a new category for testing."
    }
