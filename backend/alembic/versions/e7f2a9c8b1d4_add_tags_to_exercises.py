"""Add tags to exercises

Revision ID: e7f2a9c8b1d4
Revises: dbd337efd07e
Create Date: 2025-10-17 17:45:27.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f2a9c8b1d4'
down_revision = 'dbd337efd07e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add tags column to exercises table
    op.add_column('exercises', sa.Column('tags', sa.JSON(), nullable=False, server_default='[]'))


def downgrade() -> None:
    # Remove tags column from exercises table
    op.drop_column('exercises', 'tags')
