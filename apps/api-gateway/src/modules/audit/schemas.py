from typing import Optional
from pydantic import BaseModel

class AuditEventResponse(BaseModel):
    id: str
    tenderId: str
    bidderId: str
    documentId: Optional[str]
    complianceFlagId: Optional[str]
    officerUserId: str
    officerRole: str
    originalAiRecommendation: Optional[str]
    officerDecision: str
    officerNotes: Optional[str]
    previousDecisionState: Optional[str]
    newDecisionState: str
    createdAt: str
