"""add owner  

Revision ID: d0b116e4a312
Revises: edab9849b806
Create Date: 2026-03-19 17:01:33.037652

"""
from typing import Sequence, Union


revision: str = 'd0b116e4a312'
down_revision: Union[str, Sequence[str], None] = 'edab9849b806'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
