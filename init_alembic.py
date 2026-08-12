import io, os

# ---- 1. Create migrations/env.py ----
env_py = '''"""Alembic environment configuration."""
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.db.database import Base
from app.models import models  # noqa: F401 - ensures all models are registered on Base.metadata
from app.core.config import settings

config = context.config

# Override the sqlalchemy.url from alembic.ini with the app'"'"'s real DB settings,
# converting the async driver to the sync psycopg2 driver for migrations.
sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
config.set_main_option("sqlalchemy.url", sync_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


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


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''

with io.open("migrations/env.py", "w", encoding="utf-8") as f:
    f.write(env_py)
print("Created migrations/env.py")

# ---- 2. Create migrations/script.py.mako ----
mako = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""

with io.open("migrations/script.py.mako", "w", encoding="utf-8") as f:
    f.write(mako)
print("Created migrations/script.py.mako")

# ---- 3. Create empty versions folder ----
os.makedirs("migrations/versions", exist_ok=True)
print("Created migrations/versions/")

# ---- 4. Fix alembic.ini connection string (was pointing to wrong host/port/password) ----
path = "alembic.ini"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "sqlalchemy.url = postgresql+psycopg2://altprint:password@localhost/altprint_db"
new = "sqlalchemy.url = postgresql+psycopg2://altprint:altprint_secure_password@localhost:5433/altprint_db"
c = content.count(old)
print(f"alembic.ini URL anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("alembic.ini URL updated (note: env.py overrides this anyway using app settings)")
else:
    print("WARNING: alembic.ini anchor not found - not modified, but env.py overrides it regardless")
