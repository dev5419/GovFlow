"""Create access_logs table

Revision ID: 0005_create_access_logs
Revises: 0004_create_audit_tables
Create Date: 2026-08-31 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0005_create_access_logs'
down_revision: Union[str, None] = '0004_create_audit_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create access_logs table
    op.create_table('access_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('resource_type', sa.String(), nullable=False),
        sa.Column('resource_id', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('accessed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_logs_id'), 'access_logs', ['id'], unique=False)
    op.create_index(op.f('ix_access_logs_user_id'), 'access_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_access_logs_resource_id'), 'access_logs', ['resource_id'], unique=False)


def downgrade() -> None:
    op.drop_table('access_logs')
