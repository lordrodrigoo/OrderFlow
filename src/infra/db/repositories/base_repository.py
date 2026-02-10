from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')  # Generic type for models

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, entity_id: int) -> Optional[T]:
        return self.session.get(self.model, entity_id)

    def get_all(self) -> List[T]:
        return self.session.get(self.model).all()

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def save(self) -> None:
        # In a real application, session management is often handled at a higher level (e.g., in a service layer or via context manager)
        # to ensure all operations within a request/unit of work are in the same transaction
        self.session.commit()
