#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
from datetime import datetime
import pytest
from src.infra.db.entities.user import UserEntity



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

def test_find_user_by_id(db_session, fake_user):
    found_user = db_session.query(UserEntity).filter_by(id=fake_user.id).first()
    assert found_user is not None


def test_find_all_users(db_session, fake_user):
    users = db_session.query(UserEntity).all()
    assert len(users) >= 1

def test_uniq_email(db_session, fake_user):
    # In this test, I used fake_user to don't need to create another user
    """I insert a user with an email that already exists to test the unique constraint.
       try to commit and wait that db raise an exception (IntegrityError).
       pytest.raises(Exception) is used to check if the exception is raised.
       after that, I rollback the session to clean the state.
    """
    another_user = UserEntity(
        first_name="Carlos",
        last_name="Pereira",
        age=35,
        email="ana.silva@example.com",  # Duplicate email
        phone="192837465",
        is_active=True,
        role="user",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(another_user)
    with pytest.raises(Exception):
        db_session.commit()
    db_session.rollback()

def test_inactive_user(db_session, fake_user):
    fake_user.is_active = False
    db_session.commit()
    inactive_user = db_session.query(UserEntity).filter_by(id=fake_user.id).first()
    assert inactive_user.is_active is False


def test_user_role(db_session, fake_user):
    assert fake_user.role == "user"
