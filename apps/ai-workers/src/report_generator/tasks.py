import json
from src.queue.celery_app import celery_app
from src.report_generator.report_data_builder import ReportDataBuilder
from src.report_generator.pdf_report_builder import PDFReportBuilder
from src.report_generator.report_storage_service import ReportStorageService
from src.queue.redis_client import get_redis_client

@celery_app.task(name="report_generator.generate_compliance_report")
def generate_compliance_report(tender_id: str, bidder_id: str) -> dict:
    """
    Celery task that consumes the `report.requested` event conceptually,
    builds the report, stores it, and emits `report.generated`.
    """
    print(f"Generating compliance report for Bidder: {bidder_id}, Tender: {tender_id}")
    
    # 1. Assemble Data
    report_data = ReportDataBuilder.build_report_data(tender_id, bidder_id)
    
    # 2. Build PDF
    pdf_bytes = PDFReportBuilder.build_pdf(report_data)
    
    # 3. Store PDF
    object_key = ReportStorageService.store_report(tender_id, bidder_id, pdf_bytes)
    
    # 4. Emit Event
    r = get_redis_client()
    event_payload = {
        "tenderId": tender_id,
        "bidderId": bidder_id,
        "reportUrl": object_key,
        "status": "COMPLETED"
    }
    r.publish("report.generated", json.dumps(event_payload))
    
    print(f"Successfully generated and stored report at {object_key}")
    return {"status": "success", "object_key": object_key}
