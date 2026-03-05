"""ajusted preparation time field 

Revision ID: b7b0c22863e4
Revises: f1088bb367e1
Create Date: 2026-03-04 18:52:22.909804

"""
# pylint: disable=no-member
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = 'b7b0c22863e4'
down_revision: Union[str, Sequence[str], None] = 'f1088bb367e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('preparation_time', sa.Integer(), nullable=True))
    op.drop_column('products', 'preparation_time_minutes')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('products', sa.Column('preparation_time_minutes', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('products', 'preparation_time')
