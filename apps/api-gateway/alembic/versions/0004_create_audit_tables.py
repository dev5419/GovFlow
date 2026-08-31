"""Create users, officer decisions, and audit events tables

Revision ID: 0004_create_audit_tables
Revises: 0003_create_extracted_fields_table
Create Date: 2026-08-31 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = '0004_create_audit_tables'
down_revision: Union[str, None] = '0003_create_extracted_fields_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create users table
    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    
    # 2. Create compliance_flags table
    op.create_table('compliance_flags',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tender_id', sa.String(), nullable=False),
        sa.Column('bidder_id', sa.String(), nullable=False),
        sa.Column('rule_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('ai_recommendation', sa.String(), nullable=False),
        sa.Column('anchors', JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compliance_flags_bidder_id'), 'compliance_flags', ['bidder_id'], unique=False)
    op.create_index(op.f('ix_compliance_flags_id'), 'compliance_flags', ['id'], unique=False)
    op.create_index(op.f('ix_compliance_flags_tender_id'), 'compliance_flags', ['tender_id'], unique=False)

    # 3. Create officer_decisions table
    op.create_table('officer_decisions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('compliance_flag_id', sa.String(), nullable=False),
        sa.Column('officer_user_id', sa.String(), nullable=False),
        sa.Column('decision_state', sa.String(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['officer_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_officer_decisions_compliance_flag_id'), 'officer_decisions', ['compliance_flag_id'], unique=False)
    op.create_index(op.f('ix_officer_decisions_id'), 'officer_decisions', ['id'], unique=False)
    op.create_index(op.f('ix_officer_decisions_officer_user_id'), 'officer_decisions', ['officer_user_id'], unique=False)

    # 4. Create audit_events table
    op.create_table('audit_events',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tender_id', sa.String(), nullable=False),
        sa.Column('bidder_id', sa.String(), nullable=False),
        sa.Column('document_id', sa.String(), nullable=True),
        sa.Column('compliance_flag_id', sa.String(), nullable=True),
        sa.Column('officer_user_id', sa.String(), nullable=False),
        sa.Column('officer_role', sa.String(), nullable=False),
        sa.Column('original_ai_recommendation', sa.String(), nullable=True),
        sa.Column('officer_decision', sa.String(), nullable=False),
        sa.Column('officer_notes', sa.String(), nullable=True),
        sa.Column('previous_decision_state', sa.String(), nullable=True),
        sa.Column('new_decision_state', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_events_bidder_id'), 'audit_events', ['bidder_id'], unique=False)
    op.create_index(op.f('ix_audit_events_compliance_flag_id'), 'audit_events', ['compliance_flag_id'], unique=False)
    op.create_index(op.f('ix_audit_events_document_id'), 'audit_events', ['document_id'], unique=False)
    op.create_index(op.f('ix_audit_events_id'), 'audit_events', ['id'], unique=False)
    op.create_index(op.f('ix_audit_events_tender_id'), 'audit_events', ['tender_id'], unique=False)


def downgrade() -> None:
    op.drop_table('audit_events')
    op.drop_table('officer_decisions')
    op.drop_table('compliance_flags')
    op.drop_table('users')
