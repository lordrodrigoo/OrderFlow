"""ajusted model account 

Revision ID: e8a2c4fcb245
Revises: b7b0c22863e4
Create Date: 2026-03-12 00:50:56.747753

"""
from typing import Sequence, Union


revision: str = 'e8a2c4fcb245'
down_revision: Union[str, Sequence[str], None] = 'b7b0c22863e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
