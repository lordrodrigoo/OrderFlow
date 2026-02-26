"""ajusted models category 

Revision ID: a761787147f6
Revises: 1decb4842299
Create Date: 2026-02-26 16:38:41.017454

"""
from typing import Sequence, Union


revision: str = 'a761787147f6'
down_revision: Union[str, Sequence[str], None] = '1decb4842299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
