"""add owner_id to posts

Revision ID: 6eabb0826eb3
Revises: 6c1c303b37e2
Create Date: 2026-05-19 09:25:44.671061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6eabb0826eb3'
down_revision: Union[str, Sequence[str], None] = '6c1c303b37e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


FK_NAME = "posts_owner_id_fkey"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(FK_NAME, 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.execute("UPDATE posts SET owner_id = (SELECT id FROM users LIMIT 1)")
    op.alter_column('posts', 'owner_id', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(FK_NAME, 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
