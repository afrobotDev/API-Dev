"""ensure created_at on posts

Revision ID: 0d688aa2d3a0
Revises: 99930d0c642c
Create Date: 2026-05-17 10:24:03.502693

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0d688aa2d3a0'
down_revision: Union[str, Sequence[str], None] = '99930d0c642c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        ALTER TABLE posts
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        ALTER TABLE posts
        DROP COLUMN IF EXISTS created_at
        """
    )
