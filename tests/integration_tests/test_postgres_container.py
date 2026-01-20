from testcontainers.postgres import PostgresContainer
import sqlalchemy

def test_postgres_container_connection():
    """This test starts a Postgres container  and tests the connection.
    Obtains the connection url of database created in container.
    Creates a engine sqlalchemy and connects to the database.
    Opened a connection and executes a simple query to verify the connection.
    Asserts that the returned version string contains 'PostgreSQL'.
    """
    with PostgresContainer("postgres:16") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        with engine.connect() as connection:
            version = connection.execute(sqlalchemy.text("SELECT version();")).fetchone()
            print(version)
            assert "PostgreSQL" in version[0]
