"""ajusted create_at and update_at all entities

Revision ID: 37d9ee8a75ef
Revises: 8d2ec5f7efe8
Create Date: 2026-02-03 17:42:20.787629

"""
#pylint: disable=no-member
from typing import Sequence, Union

revision: str = '37d9ee8a75ef'
down_revision: Union[str, Sequence[str], None] = '8d2ec5f7efe8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

def downgrade() -> None:
    """Downgrade schema."""
