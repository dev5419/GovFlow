from typing import List, Optional
from pydantic import BaseModel
from govflow_shared_types import ComplianceFlagStatus, EvidenceAnchor

class ComplianceFlagResponse(BaseModel):
    id: str
    tenderId: str
    bidderId: str
    ruleId: Optional[str]
    status: str
    severity: str
    title: str
    reason: str
    aiRecommendation: str
    anchors: List[EvidenceAnchor]
    createdAt: str

class OfficerDecisionCreate(BaseModel):
    decisionState: str # Confirmed, Rejected, Overridden, Escalated
    notes: Optional[str] = None
