"""datetime in entities  

Revision ID: edab9849b806
Revises: 48a009151d1e
Create Date: 2026-03-16 18:50:27.301370

"""
from typing import Sequence, Union


revision: str = 'edab9849b806'
down_revision: Union[str, Sequence[str], None] = '48a009151d1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""



def downgrade() -> None:
    """Downgrade schema."""
