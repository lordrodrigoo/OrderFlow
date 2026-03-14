import pytest
from .connection import DBConnectionHandler

@pytest.mark.unit
def test_create_database_engine():
    db_connection_handler = DBConnectionHandler()
    engine = db_connection_handler.get_engine()
    assert engine is not None


@pytest.mark.unit
def test_get_session():
    db = DBConnectionHandler()
    session = db.get_session()
    assert session is not None
    session.close()


@pytest.mark.unit
def test_context_manager_commit():
    with DBConnectionHandler() as db:
        assert db.session is not None
    # session should be closed after exit without exception


@pytest.mark.unit
def test_context_manager_rollback():
    try:
        with DBConnectionHandler() as db:
            assert db.session is not None
            raise ValueError("force rollback")
    except ValueError:
        pass
