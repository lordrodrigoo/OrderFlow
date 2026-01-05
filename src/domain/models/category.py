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
