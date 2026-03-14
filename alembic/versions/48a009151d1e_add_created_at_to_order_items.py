"""add_created_at_to_order_items

Revision ID: 48a009151d1e
Revises: e8a2c4fcb245
Create Date: 2026-03-13 17:50:23.330107

"""
#pylint: disable=no-member
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = '48a009151d1e'
down_revision: Union[str, Sequence[str], None] = 'e8a2c4fcb245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('order_items', sa.Column('created_at', sa.DateTime(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('order_items', 'created_at')
