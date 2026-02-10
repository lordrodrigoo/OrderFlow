"""ajusted user and account 

Revision ID: 7423bd6cc880
Revises: cfd6809bd7f6
Create Date: 2026-02-10 00:36:08.544205

"""
from typing import Sequence, Union


revision: str = '7423bd6cc880'
down_revision: Union[str, Sequence[str], None] = 'cfd6809bd7f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""



def downgrade() -> None:
    """Downgrade schema."""
