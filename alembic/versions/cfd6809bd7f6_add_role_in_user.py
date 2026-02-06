#pylint: disable=no-member
"""add role in user 

Revision ID: cfd6809bd7f6
Revises: 37d9ee8a75ef
Create Date: 2026-02-06 00:37:04.651875

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = 'cfd6809bd7f6'
down_revision: Union[str, Sequence[str], None] = '37d9ee8a75ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('role', sa.String(length=20), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
