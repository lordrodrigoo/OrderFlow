from src.domain.models.user import Users, UserRole
from src.infra.db.repositories.user_repository_interface import UserRepository
from src.tests.helpers import FakeDBConnectionHandler


def test_update_user(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    user = Users.from_entity(fake_user)
    user.first_name = "Ana Updated"
    user.last_name = "Silva Updated"
    user.age = 29
    user.email = "ana.silva.souza@example.com"
    user.phone = "987654321"
    user.is_active = False
    user.role = UserRole.ADMIN

    updated_user = user_repo.update_user(user)
    assert updated_user.first_name == "Ana Updated"
    assert updated_user.last_name == "Silva Updated"
    assert updated_user.age == 29
    assert updated_user.email == "ana.silva.souza@example.com"
    assert updated_user.phone == "987654321"
    assert updated_user.is_active is False
    assert updated_user.role == UserRole.ADMIN


def test_get_user_by_role(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    users = user_repo.get_user_by_role(UserRole.USER)
    assert len(users) == 1
    assert users[0].id == fake_user.id
    assert users[0].role == UserRole.USER


def test_is_admin(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    assert user_repo.is_admin(fake_user.id) is False


def test_find_by_name(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    found_user = user_repo.find_by_name(fake_user.first_name)
    assert isinstance(found_user, list)
    assert any(user.id == fake_user.id for user in found_user)
