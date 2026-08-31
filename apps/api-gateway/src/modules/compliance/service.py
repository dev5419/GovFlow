from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.modules.compliance.repository import ComplianceRepository
from src.database.models.user import UserModel
from src.modules.compliance.schemas import ComplianceFlagResponse

class ComplianceService:
    @staticmethod
    async def get_flags(db: AsyncSession, tender_id: str, bidder_id: str) -> List[ComplianceFlagResponse]:
        flags = await ComplianceRepository.get_flags(db, tender_id, bidder_id)
        return [
            ComplianceFlagResponse(
                id=f.id,
                tenderId=f.tender_id,
                bidderId=f.bidder_id,
                ruleId=f.rule_id,
                status=f.status,
                severity=f.severity,
                title=f.title,
                reason=f.reason,
                aiRecommendation=f.ai_recommendation,
                anchors=f.anchors,
                createdAt=str(f.created_at)
            ) for f in flags
        ]

    @staticmethod
    async def record_decision(
        db: AsyncSession, 
        flag_id: str, 
        user: UserModel, 
        decision_state: str, 
        notes: Optional[str]
    ):
        flag = await ComplianceRepository.get_flag_by_id(db, flag_id)
        if not flag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flag not found")
        
        await ComplianceRepository.record_decision(db, flag, user, decision_state, notes)
        return {"message": "Decision recorded successfully"}
