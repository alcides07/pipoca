from alembic import context
from database import Base
from decouple import config as config_env
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from logging.config import fileConfig
from models.common import index

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

DATABASE_CONTAINER_ALEMBIC = str(config_env("DATABASE_CONTAINER_ALEMBIC"))
DATABASE_LOCAL = str(config_env("DATABASE_LOCAL"))
USE_DOCKER = str(config_env("USE_DOCKER"))

if (USE_DOCKER == "1"):
    config.set_main_option('sqlalchemy.url', DATABASE_CONTAINER_ALEMBIC)
else:
    config.set_main_option('sqlalchemy.url', DATABASE_LOCAL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# Interpret the config file for Python logging.
# This line sets up loggers basically.

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
