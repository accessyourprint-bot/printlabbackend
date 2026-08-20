import os

migration_content = '''"""add rider document nonce columns

Revision ID: c8e4b2f1a3d5
Revises: b7f3a1c9d2e4
Create Date: 2026-08-19 01:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "c8e4b2f1a3d5"
down_revision = "b7f3a1c9d2e4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("delivery_persons", sa.Column("driving_licence_nonce", sa.String(length=100), nullable=True))
    op.add_column("delivery_persons", sa.Column("vehicle_rc_nonce", sa.String(length=100), nullable=True))


def downgrade():
    op.drop_column("delivery_persons", "vehicle_rc_nonce")
    op.drop_column("delivery_persons", "driving_licence_nonce")
'''

path = os.path.join("migrations", "versions", "c8e4b2f1a3d5_add_rider_document_nonce_columns.py")
with open(path, "w", encoding="utf-8") as f:
    f.write(migration_content)

print(f"SUCCESS: migration written to {path}")
