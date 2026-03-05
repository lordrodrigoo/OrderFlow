from src.domain.models.category import Category
from src.infra.db.repositories.category_repository_interface import CategoryRepository
from src.tests.helpers import FakeDBConnectionHandler



def test_get_all_categories(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    category_repo = CategoryRepository(db_handler)
    categories = category_repo.get_all_categories()
    assert isinstance(categories, list)
    for category in categories:
        assert isinstance(category, Category)


def test_create_and_get_category(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    category_repo = CategoryRepository(db_handler)

    new_category = Category.create_category(
        name="Test Category",
        description="This is a test category"
    )
    created_category = category_repo.create_category(new_category)
    assert created_category.name == "Test Category"
    assert created_category.description == "This is a test category"

    retrieved_category = category_repo.get_category_by_id(created_category.id)
    assert retrieved_category is not None
    assert retrieved_category.id == created_category.id
    assert retrieved_category.name == "Test Category"
    assert retrieved_category.description == "This is a test category"


def test_update_category(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    category_repo = CategoryRepository(db_handler)

    new_category = Category.create_category(
        name="Original Category",
        description="This is the original category"
    )
    created_category = category_repo.create_category(new_category)

    created_category.name = "Updated Category"
    created_category.description = "This is the updated category"
    updated_category = category_repo.update_category(created_category)

    assert updated_category.name == "Updated Category"
    assert updated_category.description == "This is the updated category"


def test_find_category_by_name(db_session, fake_category):
    db_handler = FakeDBConnectionHandler(db_session)
    category_repo = CategoryRepository(db_handler)

    found_category = category_repo.find_category_by_name(fake_category.name)
    assert found_category is not None
    assert found_category.id == fake_category.id
    assert found_category.name == fake_category.name
    assert found_category.description == fake_category.description


def test_delete_category(db_session, fake_category):
    db_handler = FakeDBConnectionHandler(db_session)
    category_repo = CategoryRepository(db_handler)

    category_repo.delete_category(fake_category.id)
    deleted_category = category_repo.get_category_by_id(fake_category.id)
    assert deleted_category is None
