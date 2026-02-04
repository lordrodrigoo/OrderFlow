"""Remove password_hash from users

Revision ID: 8d2ec5f7efe8
Revises: 0d9bbab453b2
Create Date: 2026-02-03 17:23:57.700038

"""
#pylint: disable=no-member
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = '8d2ec5f7efe8'
down_revision: Union[str, Sequence[str], None] = '0d9bbab453b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, 'categories', ['name'])
    op.create_unique_constraint(None, 'products', ['name'])
    op.add_column('reviews', sa.Column('product_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'reviews', 'products', ['product_id'], ['id'])
    op.drop_column('users', 'password_hash')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'product_id')
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_constraint(None, 'categories', type_='unique')
