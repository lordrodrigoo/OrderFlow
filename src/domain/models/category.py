#pylint: disable=redefined-builtin

class Category:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def from_entity(cls, entity) -> "Category":
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )

    def __repr__(self):
        return f"Category [id = {self.id}, name = {self.name}]"
