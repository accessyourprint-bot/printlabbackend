"""add rider order lifecycle fields

Revision ID: c2a8f4e1b9d3
Revises: d1f6a9c3e7b2
"""
from alembic import op
import sqlalchemy as sa

revision = "c2a8f4e1b9d3"
down_revision = "d1f6a9c3e7b2"
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'accepted'")
        op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'en_route_pickup'")
        op.execute("ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'reached_pickup'")

    op.add_column("orders", sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("orders", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("orders", sa.Column("reached_pickup_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("orders", sa.Column("picked_up_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("orders", sa.Column("payout_amount", sa.Numeric(10, 2), nullable=True))
    op.add_column("orders", sa.Column("payout_recorded", sa.Boolean(), nullable=False, server_default=sa.text("false")))


def downgrade():
    op.drop_column("orders", "payout_recorded")
    op.drop_column("orders", "payout_amount")
    op.drop_column("orders", "picked_up_at")
    op.drop_column("orders", "reached_pickup_at")
    op.drop_column("orders", "started_at")
    op.drop_column("orders", "accepted_at")
