from src.domain.models.category import Category
from src.infra.db.entities.category import CategoryEntity


def test_create_category():
    category = Category.create_category(
        name="Desserts",
        description="Sweet treats to enjoy after meals"
    )
    assert isinstance(category, Category)
    assert category.name == "Desserts"
    assert category.description == "Sweet treats to enjoy after meals"


def test_from_entity():
    class MockCategoryEntity:
        def __init__(self):
            self.id = 1
            self.name = "Desserts"
            self.description = "Sweet treats to enjoy after meals"

    entity = MockCategoryEntity()
    category = Category.from_entity(entity)
    assert category.id == 1
    assert category.name == "Desserts"
    assert category.description == "Sweet treats to enjoy after meals"


def test_repr():
    category = CategoryEntity(id=1, name="Desserts")
    assert repr(category) == "CategoryEntity [id = 1, name = Desserts]"
