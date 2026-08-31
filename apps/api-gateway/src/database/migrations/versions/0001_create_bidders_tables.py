"""Create bidders and bidder_compliance_summaries tables

Revision ID: 0001
Revises: None
Create Date: 2026-08-31
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bidders",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("tender_id", sa.String(), nullable=False, index=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("registration_number", sa.String(), nullable=True),
        sa.Column("gstin", sa.String(), nullable=True),
        sa.Column("pan", sa.String(), nullable=True),
        sa.Column("udyam_number", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="submitted"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "bidder_compliance_summaries",
        sa.Column(
            "bidder_id",
            sa.String(),
            sa.ForeignKey("bidders.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("tender_id", sa.String(), nullable=False, index=True),
        sa.Column("bidder_name", sa.String(), nullable=False),
        sa.Column("compliance_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_documents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("submitted_documents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("missing_documents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("verified_flags_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("needs_review_flags_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("non_compliance_flags_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("confirmed_flags_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("unresolved_flags_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("processing_status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("primary_risk_reasons", postgresql.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("overall_status", sa.String(), nullable=False, server_default="Processing"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("bidder_compliance_summaries")
    op.drop_table("bidders")
