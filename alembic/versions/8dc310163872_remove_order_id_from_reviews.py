"""remove order_id from reviews 

Revision ID: 8dc310163872
Revises: d4014b6cf140
Create Date: 2026-03-03 17:45:59.365778

"""
# pylint: disable=no-member
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = '8dc310163872'
down_revision: Union[str, Sequence[str], None] = 'd4014b6cf140'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.drop_column('order_id')


def downgrade() -> None:
    with op.batch_alter_table('reviews') as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_reviews_order_id_orders', 'orders', ['order_id'], ['id'])
