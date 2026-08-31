from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.compliance_flag import ComplianceFlagModel
from src.database.models.officer_decision import OfficerDecisionModel
from src.database.models.audit_event import AuditEventModel
from src.database.models.user import UserModel
from fastapi import HTTPException

class ComplianceRepository:
    @staticmethod
    async def get_flags(db: AsyncSession, tender_id: str, bidder_id: str) -> List[ComplianceFlagModel]:
        stmt = select(ComplianceFlagModel).where(
            ComplianceFlagModel.tender_id == tender_id,
            ComplianceFlagModel.bidder_id == bidder_id
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_flag_by_id(db: AsyncSession, flag_id: str) -> Optional[ComplianceFlagModel]:
        stmt = select(ComplianceFlagModel).where(ComplianceFlagModel.id == flag_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def record_decision(
        db: AsyncSession, 
        flag: ComplianceFlagModel, 
        user: UserModel, 
        decision_state: str, 
        notes: Optional[str]
    ):
        """
        Records an OfficerDecision and an AuditEvent in a single transaction.
        CRITICAL CONSTRAINT: Does NOT mutate the ComplianceFlagModel.
        """
        # 1. Check previous decision state (for audit log)
        stmt = select(OfficerDecisionModel).where(
            OfficerDecisionModel.compliance_flag_id == flag.id
        ).order_by(OfficerDecisionModel.created_at.desc())
        result = await db.execute(stmt)
        prev_decision = result.scalars().first()
        prev_state = prev_decision.decision_state if prev_decision else None

        # 2. Insert OfficerDecision
        decision = OfficerDecisionModel(
            compliance_flag_id=flag.id,
            officer_user_id=user.id,
            decision_state=decision_state,
            notes=notes
        )
        db.add(decision)

        # 3. Insert AuditEvent
        document_id = None
        if flag.anchors and len(flag.anchors) > 0:
            document_id = flag.anchors[0].get("documentId") # Optional mapping for the event

        audit_event = AuditEventModel(
            tender_id=flag.tender_id,
            bidder_id=flag.bidder_id,
            document_id=document_id,
            compliance_flag_id=flag.id,
            officer_user_id=user.id,
            officer_role=user.role,
            original_ai_recommendation=flag.ai_recommendation,
            officer_decision=decision_state,
            officer_notes=notes,
            previous_decision_state=prev_state,
            new_decision_state=decision_state
        )
        db.add(audit_event)

        # 4. Commit transaction
        await db.commit()
        return decision
