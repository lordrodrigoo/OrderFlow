"""ajusted models order

Revision ID: 5a583be826cb
Revises: a761787147f6
Create Date: 2026-02-27 23:00:34.552568

"""
#pylint: disable=no-member
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = '5a583be826cb'
down_revision: Union[str, Sequence[str], None] = 'a761787147f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('orders', sa.Column('address_id', sa.Integer(), nullable=False))
    op.add_column('orders', sa.Column('delivery_fee', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('orders', sa.Column('notes', sa.String(length=255), nullable=True))
    op.add_column('orders', sa.Column('scheduled_date', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'orders', 'addresses', ['address_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'scheduled_date')
    op.drop_column('orders', 'notes')
    op.drop_column('orders', 'delivery_fee')
    op.drop_column('orders', 'address_id')
