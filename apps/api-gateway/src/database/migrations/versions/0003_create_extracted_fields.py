"""create extracted_fields table

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-31 16:42:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('extracted_fields',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('page_number', sa.Integer(), nullable=False),
    sa.Column('field_name', sa.String(), nullable=False),
    sa.Column('raw_text', sa.Text(), nullable=False),
    sa.Column('normalized_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=False),
    sa.Column('bounding_box', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('extraction_method', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extracted_fields_document_id'), 'extracted_fields', ['document_id'], unique=False)
    op.create_index(op.f('ix_extracted_fields_field_name'), 'extracted_fields', ['field_name'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_extracted_fields_field_name'), table_name='extracted_fields')
    op.drop_index(op.f('ix_extracted_fields_document_id'), table_name='extracted_fields')
    op.drop_table('extracted_fields')
