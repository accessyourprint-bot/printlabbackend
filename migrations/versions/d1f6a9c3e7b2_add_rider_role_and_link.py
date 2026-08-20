"""add rider role and link delivery_persons to users

Revision ID: d1f6a9c3e7b2
Revises: c8e4b2f1a3d5
Create Date: 2026-08-19 02:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "d1f6a9c3e7b2"
down_revision = "c8e4b2f1a3d5"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE user_role ADD VALUE IF NOT EXISTS \'rider\'")
    op.add_column("delivery_persons", sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "delivery_persons_user_id_fkey",
        "delivery_persons", "users",
        ["user_id"], ["id"],
    )
    op.create_unique_constraint("delivery_persons_user_id_key", "delivery_persons", ["user_id"])


def downgrade():
    op.drop_constraint("delivery_persons_user_id_key", "delivery_persons", type_="unique")
    op.drop_constraint("delivery_persons_user_id_fkey", "delivery_persons", type_="foreignkey")
    op.drop_column("delivery_persons", "user_id")
    # Note: removing an enum value in Postgres requires recreating the type; not handled here.
