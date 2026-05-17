"""add description to posts

Revision ID: 99930d0c642c
Revises: 9bc4bd327d73
Create Date: 2026-05-17 09:48:30.869781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99930d0c642c'
down_revision: Union[str, Sequence[str], None] = '9bc4bd327d73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "description")
