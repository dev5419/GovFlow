import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models.report import ReportModel, ReportStatus

class ReportRepository:
    
    @staticmethod
    async def create_report_record(db: AsyncSession, tender_id: str, bidder_id: str, user_id: str) -> ReportModel:
        report = ReportModel(
            id=str(uuid.uuid4()),
            tender_id=tender_id,
            bidder_id=bidder_id,
            requested_by=user_id,
            status=ReportStatus.PENDING
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def update_report_status(db: AsyncSession, report_id: str, status: ReportStatus, object_key: str = None) -> ReportModel:
        result = await db.execute(select(ReportModel).filter(ReportModel.id == report_id))
        report = result.scalar_one_or_none()
        if not report:
            return None
            
        report.status = status
        if object_key:
            report.object_key = object_key
            
        await db.commit()
        await db.refresh(report)
        return report
        
    @staticmethod
    async def update_report_status_by_bidder(db: AsyncSession, tender_id: str, bidder_id: str, status: ReportStatus, object_key: str = None) -> ReportModel:
        # If we only have bidder_id in the event (Module 7.1 tasks currently only receive tender/bidder, wait...)
        # Actually, if multiple are PENDING, we just update the most recent one.
        result = await db.execute(
            select(ReportModel)
            .filter(ReportModel.tender_id == tender_id, ReportModel.bidder_id == bidder_id, ReportModel.status == ReportStatus.PENDING)
            .order_by(ReportModel.created_at.desc())
            .limit(1)
        )
        report = result.scalar_one_or_none()
        if not report:
            return None
            
        report.status = status
        if object_key:
            report.object_key = object_key
            
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_reports_for_bidder(db: AsyncSession, tender_id: str, bidder_id: str) -> list[ReportModel]:
        result = await db.execute(
            select(ReportModel)
            .filter(ReportModel.tender_id == tender_id, ReportModel.bidder_id == bidder_id)
            .order_by(ReportModel.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: str) -> ReportModel:
        result = await db.execute(select(ReportModel).filter(ReportModel.id == report_id))
        return result.scalar_one_or_none()
