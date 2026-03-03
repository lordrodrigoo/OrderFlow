"""ajusted relationhshit between review and order 

Revision ID: f63b8269dbab
Revises: 8dc310163872
Create Date: 2026-03-03 18:00:00.393940

"""
from typing import Sequence, Union



revision: str = 'f63b8269dbab'
down_revision: Union[str, Sequence[str], None] = '8dc310163872'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
