"""create table product and categories

Revision ID: a2d1e1f78988
Revises: a5413f30bce3
Create Date: 2026-01-12 16:13:33.118518

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op


revision: str = 'a2d1e1f78988'
down_revision: Union[str, Sequence[str], None] = 'a5413f30bce3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categories',  #pylint: disable=no-member
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',  #pylint: disable=no-member
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('preparation_time_minutes', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.String(length=30), nullable=False),
    sa.Column('updated_at', sa.String(length=30), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')  #pylint: disable=no-member
    op.drop_table('categories')  #pylint: disable=no-member
