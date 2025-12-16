"""Add leaderboard tables

Revision ID: a9b4c5d6e7f8
Revises: f8a3b2c1d9e5
Create Date: 2025-12-16

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b4c5d6e7f8'
down_revision = 'f8a3b2c1d9e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create leaderboard_entries table
    op.create_table(
        'leaderboard_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('score_type', sa.Enum('xp', 'accuracy', 'streak', 'exercises_completed',
                                        name='scoretype'), nullable=False),
        sa.Column('score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('period', sa.Enum('daily', 'weekly', 'monthly', 'all_time',
                                     name='leaderboardperiod'), nullable=False),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('achieved_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for leaderboard_entries
    op.create_index(op.f('ix_leaderboard_entries_id'), 'leaderboard_entries', ['id'], unique=False)
    op.create_index(op.f('ix_leaderboard_entries_user_id'), 'leaderboard_entries', ['user_id'], unique=False)
    op.create_index(op.f('ix_leaderboard_entries_score_type'), 'leaderboard_entries', ['score_type'], unique=False)
    op.create_index(op.f('ix_leaderboard_entries_period'), 'leaderboard_entries', ['period'], unique=False)
    op.create_index(op.f('ix_leaderboard_entries_rank'), 'leaderboard_entries', ['rank'], unique=False)

    # Create composite index for efficient leaderboard queries
    op.create_index(
        'idx_leaderboard_score_period',
        'leaderboard_entries',
        ['score_type', 'period', 'score', 'achieved_at'],
        unique=False
    )

    # Create composite index for user-specific queries
    op.create_index(
        'idx_leaderboard_user_period',
        'leaderboard_entries',
        ['user_id', 'score_type', 'period'],
        unique=False
    )

    # Create leaderboard_snapshots table
    op.create_table(
        'leaderboard_snapshots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('score_type', sa.Enum('xp', 'accuracy', 'streak', 'exercises_completed',
                                        name='scoretype'), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('period', sa.Enum('daily', 'weekly', 'monthly', 'all_time',
                                     name='leaderboardperiod'), nullable=False),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('snapshot_date', sa.DateTime(), nullable=False),
        sa.Column('total_participants', sa.Integer(), nullable=False),
        sa.Column('percentile', sa.Float(), nullable=True),
        sa.Column('score_change', sa.Float(), nullable=True),
        sa.Column('rank_change', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for leaderboard_snapshots
    op.create_index(op.f('ix_leaderboard_snapshots_id'), 'leaderboard_snapshots', ['id'], unique=False)
    op.create_index(op.f('ix_leaderboard_snapshots_user_id'), 'leaderboard_snapshots', ['user_id'], unique=False)
    op.create_index(op.f('ix_leaderboard_snapshots_score_type'), 'leaderboard_snapshots', ['score_type'], unique=False)
    op.create_index(op.f('ix_leaderboard_snapshots_period'), 'leaderboard_snapshots', ['period'], unique=False)
    op.create_index(op.f('ix_leaderboard_snapshots_rank'), 'leaderboard_snapshots', ['rank'], unique=False)
    op.create_index(op.f('ix_leaderboard_snapshots_snapshot_date'), 'leaderboard_snapshots', ['snapshot_date'], unique=False)

    # Create composite index for historical queries
    op.create_index(
        'idx_snapshot_period_type',
        'leaderboard_snapshots',
        ['period', 'score_type', 'snapshot_date'],
        unique=False
    )

    # Create composite index for user history
    op.create_index(
        'idx_snapshot_user_history',
        'leaderboard_snapshots',
        ['user_id', 'score_type', 'period', 'snapshot_date'],
        unique=False
    )

    # Create leaderboard_cache table
    op.create_table(
        'leaderboard_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('score_type', sa.Enum('xp', 'accuracy', 'streak', 'exercises_completed',
                                        name='scoretype'), nullable=False),
        sa.Column('period', sa.Enum('daily', 'weekly', 'monthly', 'all_time',
                                     name='leaderboardperiod'), nullable=False),
        sa.Column('cache_key', sa.String(255), nullable=False),
        sa.Column('cached_data', sa.String(), nullable=False),
        sa.Column('cache_hits', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for leaderboard_cache
    op.create_index(op.f('ix_leaderboard_cache_id'), 'leaderboard_cache', ['id'], unique=False)
    op.create_index(op.f('ix_leaderboard_cache_score_type'), 'leaderboard_cache', ['score_type'], unique=False)
    op.create_index(op.f('ix_leaderboard_cache_period'), 'leaderboard_cache', ['period'], unique=False)
    op.create_index(op.f('ix_leaderboard_cache_cache_key'), 'leaderboard_cache', ['cache_key'], unique=True)
    op.create_index(op.f('ix_leaderboard_cache_expires_at'), 'leaderboard_cache', ['expires_at'], unique=False)


def downgrade() -> None:
    # Drop leaderboard_cache table
    op.drop_index(op.f('ix_leaderboard_cache_expires_at'), table_name='leaderboard_cache')
    op.drop_index(op.f('ix_leaderboard_cache_cache_key'), table_name='leaderboard_cache')
    op.drop_index(op.f('ix_leaderboard_cache_period'), table_name='leaderboard_cache')
    op.drop_index(op.f('ix_leaderboard_cache_score_type'), table_name='leaderboard_cache')
    op.drop_index(op.f('ix_leaderboard_cache_id'), table_name='leaderboard_cache')
    op.drop_table('leaderboard_cache')

    # Drop leaderboard_snapshots table
    op.drop_index('idx_snapshot_user_history', table_name='leaderboard_snapshots')
    op.drop_index('idx_snapshot_period_type', table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_snapshot_date'), table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_rank'), table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_period'), table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_score_type'), table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_user_id'), table_name='leaderboard_snapshots')
    op.drop_index(op.f('ix_leaderboard_snapshots_id'), table_name='leaderboard_snapshots')
    op.drop_table('leaderboard_snapshots')

    # Drop leaderboard_entries table
    op.drop_index('idx_leaderboard_user_period', table_name='leaderboard_entries')
    op.drop_index('idx_leaderboard_score_period', table_name='leaderboard_entries')
    op.drop_index(op.f('ix_leaderboard_entries_rank'), table_name='leaderboard_entries')
    op.drop_index(op.f('ix_leaderboard_entries_period'), table_name='leaderboard_entries')
    op.drop_index(op.f('ix_leaderboard_entries_score_type'), table_name='leaderboard_entries')
    op.drop_index(op.f('ix_leaderboard_entries_user_id'), table_name='leaderboard_entries')
    op.drop_index(op.f('ix_leaderboard_entries_id'), table_name='leaderboard_entries')
    op.drop_table('leaderboard_entries')

    # Drop enums (note: may need adjustment based on your database)
    # For PostgreSQL:
    sa.Enum(name='scoretype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='leaderboardperiod').drop(op.get_bind(), checkfirst=True)
