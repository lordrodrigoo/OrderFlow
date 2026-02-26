"""ajusted models category 

Revision ID: 1decb4842299
Revises: 2e9d7353fe8f
Create Date: 2026-02-26 15:33:57.887649

"""
from typing import Sequence, Union


revision: str = '1decb4842299'
down_revision: Union[str, Sequence[str], None] = '2e9d7353fe8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
