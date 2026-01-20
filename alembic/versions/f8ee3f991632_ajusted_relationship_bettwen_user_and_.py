#pylint: disable=no-member
"""ajusted relationship bettwen user and account

Revision ID: f8ee3f991632
Revises: 3be9f4a35cbf
Create Date: 2026-01-19 23:51:51.797966

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = 'f8ee3f991632'
down_revision: Union[str, Sequence[str], None] = '3be9f4a35cbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('accounts', 'user_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('accounts', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
