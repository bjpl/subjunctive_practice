"""Add user_settings table

Revision ID: f8a3b2c1d9e5
Revises: e7f2a9c8b1d4
Create Date: 2025-12-02

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8a3b2c1d9e5'
down_revision = 'e7f2a9c8b1d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_settings table
    op.create_table('user_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('notifications', sa.JSON(), nullable=False,
                  server_default='{"email": true, "push": false, "streakReminders": true}'),
        sa.Column('practice', sa.JSON(), nullable=False,
                  server_default='{"dailyGoal": 10, "autoAdvance": true, "showHints": true, "showExplanations": true}'),
        sa.Column('accessibility', sa.JSON(), nullable=False,
                  server_default='{"fontSize": "medium", "highContrast": false, "reduceMotion": false}'),
        sa.Column('language', sa.JSON(), nullable=False,
                  server_default='{"interface": "en", "practice": "es"}'),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_settings_id'), 'user_settings', ['id'], unique=False)
    op.create_index(op.f('ix_user_settings_user_id'), 'user_settings', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_settings_user_id'), table_name='user_settings')
    op.drop_index(op.f('ix_user_settings_id'), table_name='user_settings')
    op.drop_table('user_settings')
