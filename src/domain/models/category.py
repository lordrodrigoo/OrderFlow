#pylint: disable=redefined-builtin
from typing import Optional
from dataclasses import dataclass

@dataclass
class Category:
    name: str
    description: str
    id: Optional[int] = None

    @classmethod
    def from_entity(cls, entity) -> "Category":
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )


    def __repr__(self):
        return f"Category [id = {self.id}, name = {self.name}]"
