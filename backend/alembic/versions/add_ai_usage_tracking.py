"""Add AI usage tracking table

Revision ID: ai_usage_001
Revises: f8a3b2c1d9e5
Create Date: 2025-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Index


# revision identifiers, used by Alembic.
revision = 'ai_usage_001'
down_revision = 'f8a3b2c1d9e5'
branch_labels = None
depends_on = None


def upgrade():
    """Create ai_usage_records table."""
    op.create_table(
        'ai_usage_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('request_type', sa.String(length=50), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False, server_default='claude-3-5-sonnet-20241022'),
        sa.Column('input_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('output_tokens', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for common query patterns
    op.create_index('ix_ai_usage_records_id', 'ai_usage_records', ['id'])
    op.create_index('ix_ai_usage_records_user_id', 'ai_usage_records', ['user_id'])
    op.create_index('ix_ai_usage_records_request_type', 'ai_usage_records', ['request_type'])
    op.create_index('ix_ai_usage_records_created_at', 'ai_usage_records', ['created_at'])

    # Composite indexes for common queries
    op.create_index('idx_user_date', 'ai_usage_records', ['user_id', 'created_at'])
    op.create_index('idx_type_date', 'ai_usage_records', ['request_type', 'created_at'])
    op.create_index('idx_date_cost', 'ai_usage_records', ['created_at', 'estimated_cost'])


def downgrade():
    """Drop ai_usage_records table and indexes."""
    op.drop_index('idx_date_cost', table_name='ai_usage_records')
    op.drop_index('idx_type_date', table_name='ai_usage_records')
    op.drop_index('idx_user_date', table_name='ai_usage_records')
    op.drop_index('ix_ai_usage_records_created_at', table_name='ai_usage_records')
    op.drop_index('ix_ai_usage_records_request_type', table_name='ai_usage_records')
    op.drop_index('ix_ai_usage_records_user_id', table_name='ai_usage_records')
    op.drop_index('ix_ai_usage_records_id', table_name='ai_usage_records')
    op.drop_table('ai_usage_records')
