from typing import List, Optional
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.category import CategoryEntity
from src.domain.repositories.category_repository import CategoryRepository
from src.domain.models.category import Category
from src.infra.db.repositories.base_repository import BaseRepository


class CategoryRepositoryInterface(CategoryRepository, BaseRepository[CategoryEntity]):
    def __init__(self, db_connection: DBConnectionHandler):
        super().__init__(db_connection.get_session(), CategoryEntity)

    def create_category(self, category: Category) -> Category:
        entity = CategoryEntity(
            name=category.name,
            description=category.description
        )
        self.add(entity)
        self.save()

        return Category.from_entity(entity)

    def update_category(self, category: Category) -> Optional[Category]:
        if category.id is None:
            raise ValueError("Category ID must be provided for update.")
        entity = self.get_by_id(category.id)
        if not entity:
            return None

        entity.name = category.name
        entity.description = category.description
        self.save()

        return Category.from_entity(entity)

    def find_all_categories(self) -> List[Category]:
        return [Category.from_entity(entity) for entity in self.get_all()]

    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        entity = self.get_by_id(category_id)
        return Category.from_entity(entity) if entity else None

    def delete_category(self, category_id: int) -> bool:
        entity = self.get_by_id(category_id)

        if entity:
            self.delete(entity)
            self.save()
            return True
        return False
