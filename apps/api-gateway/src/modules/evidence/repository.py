from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.extracted_field import ExtractedFieldModel
from src.database.models.compliance_flag import ComplianceFlagModel
from src.database.models.audit_event import AccessLogModel

class EvidenceRepository:
    
    @staticmethod
    async def log_access(
        db: AsyncSession,
        user_id: str,
        resource_type: str,
        resource_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> AccessLogModel:
        """
        Logs a read/access event to satisfy PRD 21.2/21.3.
        """
        log_entry = AccessLogModel(
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry

    @staticmethod
    async def get_fields_for_page(db: AsyncSession, document_id: str, page_number: int) -> List[ExtractedFieldModel]:
        """
        Fetch extracted fields for a specific page.
        """
        stmt = select(ExtractedFieldModel).where(
            ExtractedFieldModel.document_id == document_id,
            ExtractedFieldModel.page_number == page_number
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_flags_for_document(db: AsyncSession, document_id: str) -> List[ComplianceFlagModel]:
        """
        Fetch all compliance flags that might have anchors on this document.
        We fetch flags where ANY anchor points to this document.
        In a relational DB, if anchors are stored as JSONB, we query the JSON structure.
        For SQLite/standard JSON, we might fetch all flags for the bidder or tender and filter in memory,
        but typically we can use a JSON operator if Postgres is used. 
        Since this is an abstraction, let's fetch by document_id if we assume there's a backref, 
        or we fetch flags by tender_id/bidder_id and filter anchors.
        For simplicity, we will query all flags for the document.
        Wait, ComplianceFlag doesn't have a direct `document_id` column because it spans multiple documents (GSTIN match).
        We should probably query by tender_id, bidder_id and filter in memory if the JSON query isn't generic.
        Let's assume we pass bidder_id and tender_id down from the router, or we query all flags.
        Actually, we can just do a broad query or require bidder_id/tender_id in the API.
        Let's just require tender_id and bidder_id for overlays to be safe and fast.
        """
        pass
        
    @staticmethod
    async def get_flags_by_bidder(db: AsyncSession, tender_id: str, bidder_id: str) -> List[ComplianceFlagModel]:
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
