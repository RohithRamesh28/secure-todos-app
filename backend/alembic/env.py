from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Add the project directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Base and models
from app.database import Base  # <-- Your SQLAlchemy Base
from app.models import Note  # <-- Import your models here

# Set target_metadata to Base.metadata for autogenerate to work
target_metadata = Base.metadata  # <-- Correct this line

# Alembic Config object provides access to values in the .ini file
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Function for offline migration (without a live connection)
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Function for online migration (with a live connection)
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if the migration is offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
