from typing import List, Optional
from pydantic import BaseModel
from govflow_shared_types import ProcessingJob, Document


class DocumentUploadResponse(BaseModel):
    tender_id: str
    bidder_id: Optional[str] = None
    job_id: str
    status: str
    message: str


class ProcessingJobResponse(BaseModel):
    job: ProcessingJob
