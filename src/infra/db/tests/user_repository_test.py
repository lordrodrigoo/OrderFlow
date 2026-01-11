import pytest
from sqlalchemy import text
from src.infra.db.repositories.user_repository import UserRepository
from src.infra.db.settings.connection import DBConnectionHandler

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()

@pytest.mark.skip(reason='Sensitive test')
def test_insert_user():
    mocked_first_name = "Alice"
    mocked_last_name = "Smith"
    mocked_password_hash = "hashed_password_123"
    mocked_age = 28
    mocked_phone = "0987654321"
    mocked_email = "alice.smith@example.com"
    mocked_is_active = True
    mocked_created_at = "2024-02-01T10:00:00"
    mocked_updated_at = "2024-02-01T10:00:00"

    user_repository = UserRepository()
    user_repository.insert_user(
        first_name=mocked_first_name,
        last_name=mocked_last_name,
        password_hash=mocked_password_hash,
        age=mocked_age,
        phone=mocked_phone,
        email=mocked_email,
        is_active=mocked_is_active,
        created_at=mocked_created_at,
        updated_at=mocked_updated_at
    )

    sql = '''
        SELECT * FROM users
        WHERE first_name = '{}'
        AND last_name = '{}'
        AND age = {}
    '''.format(mocked_first_name, mocked_last_name, mocked_age)
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.first_name == mocked_first_name
    assert registry.last_name == mocked_last_name
    assert registry.age == mocked_age

    connection.execute(text(f'''
        DELETE FROM users WHERE id = '{registry.id}'
    '''))
    connection.commit()
