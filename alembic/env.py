import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Ajouter le dossier src ou racine si nécessaire
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.settings import settings  # ton settings.py
from src.data.models import Base  # ton Base de models.py


print(settings)
print("----------------")
# Alembic Config object
config = context.config

# Logging config
fileConfig(config.config_file_name or "alembic.ini")

# metadata pour autogenerate
target_metadata = Base.metadata

def get_url():
    return settings.database_url

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
    config.get_section(config.config_ini_section) or {},  # <-- ici
    url=get_url(),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
