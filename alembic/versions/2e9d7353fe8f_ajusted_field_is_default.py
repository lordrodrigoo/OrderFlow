"""ajusted field is default 

Revision ID: 2e9d7353fe8f
Revises: 7423bd6cc880
Create Date: 2026-02-11 00:50:45.174556

"""
from typing import Sequence, Union

revision: str = '2e9d7353fe8f'
down_revision: Union[str, Sequence[str], None] = '7423bd6cc880'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
