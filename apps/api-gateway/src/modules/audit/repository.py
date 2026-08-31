from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models.audit_event import AuditEventModel

class AuditRepository:
    @staticmethod
    async def get_by_flag(db: AsyncSession, flag_id: str) -> List[AuditEventModel]:
        stmt = select(AuditEventModel).where(
            AuditEventModel.compliance_flag_id == flag_id
        ).order_by(AuditEventModel.created_at.asc())
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_bidder(db: AsyncSession, bidder_id: str) -> List[AuditEventModel]:
        stmt = select(AuditEventModel).where(
            AuditEventModel.bidder_id == bidder_id
        ).order_by(AuditEventModel.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().all()
