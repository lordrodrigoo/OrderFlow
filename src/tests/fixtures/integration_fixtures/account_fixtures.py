from datetime import datetime
import pytest
from src.infra.db.entities.account import AccountEntity
from src.config.security import hash_password

@pytest.fixture
def fake_account(db_session, fake_user):
    account = AccountEntity(
        user_id=fake_user.id,
        username="ana_silva",
        password_hash=hash_password("StrongPassword123!"),
        status="active",
        created_at=datetime.now(),
        updated_at=None
    )
    db_session.add(account)
    db_session.commit()
    return account


@pytest.fixture
def valid_account_data(fake_user):
    return {
        "user_id": fake_user.id,
        "username": "ana_silva",
        "password": "StrongPassword123!",
        "status": "active"
    }
