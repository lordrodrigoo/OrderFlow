"""add created_at to order_item

Revision ID: 13e2378b4e7e
Revises: 5a583be826cb
Create Date: 2026-03-02 17:45:51.203429

"""
from typing import Sequence, Union


revision: str = '13e2378b4e7e'
down_revision: Union[str, Sequence[str], None] = '5a583be826cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
