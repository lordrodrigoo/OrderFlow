"""ajusted models review ( removed order id field ) 

Revision ID: d4014b6cf140
Revises: 13e2378b4e7e
Create Date: 2026-03-03 17:12:23.524957

"""
from typing import Sequence, Union


revision: str = 'd4014b6cf140'
down_revision: Union[str, Sequence[str], None] = '13e2378b4e7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
