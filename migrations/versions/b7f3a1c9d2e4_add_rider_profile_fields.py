"""add rider profile fields

Revision ID: b7f3a1c9d2e4
Revises: 0f26a7a8c59e
Create Date: 2026-08-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "b7f3a1c9d2e4"
down_revision = "0f26a7a8c59e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("delivery_persons", sa.Column("city", sa.String(length=255), nullable=True))
    op.add_column("delivery_persons", sa.Column("driving_licence_url", sa.String(length=500), nullable=True))
    op.add_column("delivery_persons", sa.Column("vehicle_rc_url", sa.String(length=500), nullable=True))
    op.add_column("delivery_persons", sa.Column("orders_completed", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("delivery_persons", sa.Column("total_earned", sa.Numeric(10, 2), nullable=False, server_default="0"))


def downgrade():
    op.drop_column("delivery_persons", "total_earned")
    op.drop_column("delivery_persons", "orders_completed")
    op.drop_column("delivery_persons", "vehicle_rc_url")
    op.drop_column("delivery_persons", "driving_licence_url")
    op.drop_column("delivery_persons", "city")
