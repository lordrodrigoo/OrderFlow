from typing import List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.category import Category as CategoryEntity
from src.data.interfaces.category_repository import CategoryRepositoryInterface

class CategoryRepository(CategoryRepositoryInterface):

    @classmethod
    def insert_category(
        cls,
        name: str,
        description: str
    ) -> CategoryEntity:
        with DBConnectionHandler() as db_connection:
            try:
                new_registry = CategoryEntity(
                   id = id,
                   name = name,
                   description = description
                )
                db_connection.session.add(new_registry)
                db_connection.session.commit()
                return new_registry
            except Exception as exception:
                db_connection.session.rollback()
                raise exception

    @classmethod
    def select_category(cls, name: str) -> List[CategoryEntity]:
        with DBConnectionHandler() as db_connection:
            try:
                categories = (
                    db_connection.session
                    .query(CategoryEntity)
                    .filter(CategoryEntity.name == name)
                    .all()
                )
                return categories
            except Exception as exception:
                db_connection.session.rollback()
                raise exception
