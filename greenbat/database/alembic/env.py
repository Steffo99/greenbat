import logging.config
import alembic

import greenbat.database.base
import greenbat.database.engine
import greenbat.config


# Set up logging
logging.config.fileConfig(alembic.context.config.config_file_name)


# Get the metadata
target_metadata = greenbat.database.base.Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    alembic.context.configure(
        url=greenbat.config.cfg["database.uri"],
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with greenbat.database.engine.engine.connect() as connection:
        alembic.context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
