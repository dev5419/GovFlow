"""create reports table

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-31 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('reports',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tender_id', sa.String(), nullable=False),
        sa.Column('bidder_id', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='reportstatus'), nullable=False),
        sa.Column('object_key', sa.String(), nullable=True),
        sa.Column('requested_by', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reports_bidder_id'), 'reports', ['bidder_id'], unique=False)
    op.create_index(op.f('ix_reports_id'), 'reports', ['id'], unique=False)
    op.create_index(op.f('ix_reports_tender_id'), 'reports', ['tender_id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_reports_tender_id'), table_name='reports')
    op.drop_index(op.f('ix_reports_id'), table_name='reports')
    op.drop_index(op.f('ix_reports_bidder_id'), table_name='reports')
    op.drop_table('reports')
    op.execute('DROP TYPE reportstatus')
