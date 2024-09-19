from __future__ import with_statement
import logging
from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from alembic import context
from alembic import op
import sqlalchemy as sa

# Load configuration from the file
config = context.config
fileConfig(config.config_file_name)

# Get the target metadata
target_metadata = None

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
