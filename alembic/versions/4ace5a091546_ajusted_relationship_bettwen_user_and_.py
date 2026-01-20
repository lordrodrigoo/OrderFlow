#pylint: disable=no-member
"""ajusted relationship bettwen user and account

Revision ID: 4ace5a091546
Revises: f8ee3f991632
Create Date: 2026-01-19 23:59:40.183620

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = '4ace5a091546'
down_revision: Union[str, Sequence[str], None] = 'f8ee3f991632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('accounts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'accounts', 'users', ['user_id'], ['id'])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.drop_column('accounts', 'user_id')
