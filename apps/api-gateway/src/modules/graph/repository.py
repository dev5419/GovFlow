from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models.bidder import BidderModel
from src.database.models.document import DocumentModel, ProcessingJobModel
from src.database.models.compliance_flag import ComplianceFlagModel

class GraphRepository:
    
    @staticmethod
    async def get_bidder(db: AsyncSession, bidder_id: str) -> Optional[BidderModel]:
        stmt = select(BidderModel).where(BidderModel.id == bidder_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_documents_by_bidder(db: AsyncSession, tender_id: str, bidder_id: str) -> List[DocumentModel]:
        stmt = select(DocumentModel).where(
            DocumentModel.tender_id == tender_id,
            DocumentModel.bidder_id == bidder_id
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_processing_job(db: AsyncSession, document_id: str) -> Optional[ProcessingJobModel]:
        stmt = select(ProcessingJobModel).where(
            ProcessingJobModel.document_id == document_id
        ).order_by(ProcessingJobModel.created_at.desc())
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_compliance_flags(db: AsyncSession, tender_id: str, bidder_id: str) -> List[ComplianceFlagModel]:
        stmt = select(ComplianceFlagModel).where(
            ComplianceFlagModel.tender_id == tender_id,
            ComplianceFlagModel.bidder_id == bidder_id
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_tender_requirements(db: AsyncSession, tender_id: str) -> List[str]:
        # STUB: In a full app, this would query a TenderRuleModel.
        # Returning default mandatory requirements for graph node generation.
        return ["GST_CERTIFICATE", "PAN_CARD", "FINANCIAL_STATEMENT"]
