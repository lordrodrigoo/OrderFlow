import pytest
from src.infra.db.settings.connection import DBConnectionHandler

@pytest.fixture(scope="module")
def db_connection():
    handler = DBConnectionHandler()
    conn = handler.get_engine().connect()
    yield conn
    conn.close()
