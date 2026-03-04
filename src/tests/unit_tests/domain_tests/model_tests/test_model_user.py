from datetime import datetime
from unittest.mock import Mock
from src.domain.models.user import Users, UserRole



def test_create_user():
    user = Users.create_user(
        first_name="Jane",
        last_name="Smith",
        age=25,
        phone="0987654321",
        email="jane.smith@example.com",
        is_active=True,
        role=UserRole.USER
    )
    assert user.full_name == "Jane Smith"
    assert user.role == UserRole.USER
    assert user.is_active is True


def test_from_entity():
    user_entity = Mock(
        id=1,
        first_name="Alice",
        last_name="Johnson",
        age=28,
        phone="5555555555",
        email="alice.johnson@example.com",
        is_active=True,
        role=UserRole.USER,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    user = Users.from_entity(user_entity)
    assert user.id == 1
    assert user.full_name == "Alice Johnson"
    assert user.role == UserRole.USER
