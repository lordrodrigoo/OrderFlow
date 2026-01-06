from abc import ABC, abstractmethod
from src.domain.models.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def get_all_categories(self) -> list[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Category | None:
        pass
