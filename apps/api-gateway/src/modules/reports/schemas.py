from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.database.models.report import ReportStatus

class ReportResponse(BaseModel):
    id: str
    tender_id: str
    bidder_id: str
    status: ReportStatus
    requested_by: str
    created_at: datetime
    updated_at: datetime
    
    # Only present if status == COMPLETED
    download_url: Optional[str] = None

    class Config:
        from_attributes = True
