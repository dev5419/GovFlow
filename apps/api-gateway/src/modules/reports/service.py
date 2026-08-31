from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.reports.repository import ReportRepository
from src.database.models.report import ReportStatus, ReportModel
from src.modules.ingestion.signed_url_service import generate_presigned_url
from src.events.celery_client import celery_app

class ReportService:
    @staticmethod
    async def request_report(db: AsyncSession, tender_id: str, bidder_id: str, user_id: str) -> ReportModel:
        """
        Creates a new PENDING report record and sends a Celery task.
        """
        report = await ReportRepository.create_report_record(db, tender_id, bidder_id, user_id)
        
        # Publish to Celery
        celery_app.send_task(
            "report_generator.generate_compliance_report",
            kwargs={"tender_id": tender_id, "bidder_id": bidder_id}
        )
        
        return report

    @staticmethod
    def _attach_download_url(report: ReportModel) -> dict:
        data = {
            "id": report.id,
            "tender_id": report.tender_id,
            "bidder_id": report.bidder_id,
            "status": report.status,
            "requested_by": report.requested_by,
            "created_at": report.created_at,
            "updated_at": report.updated_at,
            "download_url": None
        }
        
        if report.status == ReportStatus.COMPLETED and report.object_key:
            data["download_url"] = generate_presigned_url("govflow-documents", report.object_key, expires_in=3600)
            
        return data

    @staticmethod
    async def get_reports(db: AsyncSession, tender_id: str, bidder_id: str) -> list[dict]:
        """
        Returns all reports for a bidder, injecting download URLs for completed ones.
        """
        reports = await ReportRepository.get_reports_for_bidder(db, tender_id, bidder_id)
        return [ReportService._attach_download_url(r) for r in reports]

    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: str) -> dict:
        report = await ReportRepository.get_report_by_id(db, report_id)
        if not report:
            return None
        return ReportService._attach_download_url(report)
