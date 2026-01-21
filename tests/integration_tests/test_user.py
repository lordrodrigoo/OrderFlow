#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
from datetime import datetime
import pytest
from src.infra.db.entities.user import UserEntity


@pytest.fixture
def fake_user(db_session):
    user = UserEntity(
        first_name="Ana",
        last_name="Silva",
        age=28,
        email="ana.silva@example.com",
        phone="123456789",
        is_active=True,
        password_hash="hashed_password",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_insert_user(db_session, fake_user):
    assert fake_user.id is not None
    assert fake_user.first_name == "Ana"
    assert fake_user.last_name == "Silva"
    assert fake_user.email == "ana.silva@example.com"

def test_update_user(db_session, fake_user):
    fake_user.last_name = "Souza"
    db_session.commit()
    updated_user = db_session.query(UserEntity).filter_by(id=fake_user.id).first()
    assert updated_user.last_name == "Souza"

def test_delete_user(db_session, fake_user):
    db_session.delete(fake_user)
    db_session.commit()
    delete_user = db_session.query(UserEntity).filter_by(id=fake_user.id).first()
    assert delete_user is None
