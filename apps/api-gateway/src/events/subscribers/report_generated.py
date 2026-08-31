import json
import logging
from src.database.session import AsyncSessionLocal
from src.modules.reports.repository import ReportRepository
from src.database.models.report import ReportStatus

logger = logging.getLogger(__name__)

async def handle_report_generated_event(message: dict):
    """
    Subscribes to `report.generated` and updates the ReportModel with the MinIO key.
    """
    try:
        data = json.loads(message["data"])
        tender_id = data.get("tenderId")
        bidder_id = data.get("bidderId")
        report_url = data.get("reportUrl")
        
        if not tender_id or not bidder_id or not report_url:
            logger.error(f"Malformed report.generated event: {data}")
            return
            
        async with AsyncSessionLocal() as db:
            # The AI worker didn't receive the explicit report_id (yet), 
            # so we update the latest PENDING report for this bidder.
            updated = await ReportRepository.update_report_status_by_bidder(
                db, 
                tender_id, 
                bidder_id, 
                ReportStatus.COMPLETED, 
                report_url
            )
            
            if updated:
                logger.info(f"Marked report {updated.id} as COMPLETED")
            else:
                logger.warning(f"No PENDING report found for bidder {bidder_id}")
                
    except Exception as e:
        logger.error(f"Error processing report.generated event: {e}")
