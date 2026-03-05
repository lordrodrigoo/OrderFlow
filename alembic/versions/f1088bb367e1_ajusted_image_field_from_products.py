"""ajusted image field from products 

Revision ID: f1088bb367e1
Revises: f63b8269dbab
Create Date: 2026-03-04 18:46:03.917127

"""
from typing import Sequence, Union


revision: str = 'f1088bb367e1'
down_revision: Union[str, Sequence[str], None] = 'f63b8269dbab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
