from abc import ABC, abstractmethod
from src.domain.models.category import Category


class CategoryRepositoryInterface(ABC):
    """This interface defines the contract for category repository."""
    @abstractmethod
    def get_all_categories(self) -> list[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    def find_category_by_name(self, name: str) -> Category | None:
        pass

    @abstractmethod
    def create_category(self, category: Category) -> Category:
        pass

    @abstractmethod
    def update_category(self, category: Category) -> Category | None:
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> bool:
        pass
