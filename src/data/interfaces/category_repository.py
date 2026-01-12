from typing import List
from abc import ABC, abstractmethod
from src.domain.models.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def insert_category(self, name: str, description: str) -> Category:
        pass

    @abstractmethod
    def select_category(self, name: str) -> List[Category]: pass
