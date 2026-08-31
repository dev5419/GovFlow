from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.audit.repository import AuditRepository
from src.modules.audit.schemas import AuditEventResponse

class AuditService:
    @staticmethod
    async def get_by_flag(db: AsyncSession, flag_id: str) -> List[AuditEventResponse]:
        events = await AuditRepository.get_by_flag(db, flag_id)
        return [AuditService._map(e) for e in events]
        
    @staticmethod
    async def get_by_bidder(db: AsyncSession, bidder_id: str) -> List[AuditEventResponse]:
        events = await AuditRepository.get_by_bidder(db, bidder_id)
        return [AuditService._map(e) for e in events]

    @staticmethod
    def _map(e) -> AuditEventResponse:
        return AuditEventResponse(
            id=e.id,
            tenderId=e.tender_id,
            bidderId=e.bidder_id,
            documentId=e.document_id,
            complianceFlagId=e.compliance_flag_id,
            officerUserId=e.officer_user_id,
            officerRole=e.officer_role,
            originalAiRecommendation=e.original_ai_recommendation,
            officerDecision=e.officer_decision,
            officerNotes=e.officer_notes,
            previousDecisionState=e.previous_decision_state,
            newDecisionState=e.new_decision_state,
            createdAt=str(e.created_at)
        )
