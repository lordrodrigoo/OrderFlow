import sys
import os

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from src.infra.db.entities import user, product, category, address # pylint: disable=unused-import
from src.infra.db.settings.base import Base # noqa: F401

from dotenv import load_dotenv # pylint: disable=wrong-import-order
load_dotenv()

# CONFIG DATABASE TO ALEMBIC WITH ENV VARIABLE
ALEMBIC_DB_URL = os.getenv("ALEMBIC_DB_URL")
if ALEMBIC_DB_URL:
    context.config.set_main_option("sqlalchemy.url", ALEMBIC_DB_URL) # pylint: disable=no-member.


target_metadata = Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config # pylint: disable=no-member


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure( # pylint: disable=no-member
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction(): # pylint: disable=no-member
        context.run_migrations() # pylint: disable=no-member


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure( # pylint: disable=no-member
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction(): # pylint: disable=no-member
            context.run_migrations() # pylint: disable=no-member


if context.is_offline_mode(): # pylint: disable=no-member
    run_migrations_offline()
else:
    run_migrations_online()
