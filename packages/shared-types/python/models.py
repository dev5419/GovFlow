"""
GovFlow Shared Types — Pydantic v2 Models
Authoritative shared types matching GovFlow_PRD.md §10, §12, §8, and §9.
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# Enums
# ============================================================================

class ComplianceFlagStatus(str, Enum):
    """Compliance flag status union per PRD §8.4 and §12.4"""
    VERIFIED = "Verified"
    POTENTIAL_NON_COMPLIANCE = "Potential Non-Compliance"
    NEEDS_REVIEW = "Needs Review"
    INSUFFICIENT_EVIDENCE = "Insufficient Evidence"
    MISSING = "Missing"


class SeverityLevel(str, Enum):
    """Finding risk severity level per PRD §12.4"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class OfficerDecisionState(str, Enum):
    """Officer decision states per PRD §9.1"""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    REJECTED = "Rejected"
    OVERRIDDEN = "Overridden"
    ESCALATED = "Escalated"


class HighlightColor(str, Enum):
    """Visual evidence highlight overlay colors per PRD §8.6"""
    RED = "red"
    AMBER = "amber"
    GREEN = "green"
    BLUE = "blue"


class GraphNodeStatus(str, Enum):
    """Interactive star graph node status per PRD §8.5"""
    VERIFIED = "Verified"
    POTENTIAL_NON_COMPLIANCE = "Potential Non-Compliance"
    CONFIRMED_NON_COMPLIANCE = "Confirmed Non-Compliance"
    NEEDS_REVIEW = "Needs Review"
    INSUFFICIENT_EVIDENCE = "Insufficient Evidence"
    MISSING = "Missing"
    PROCESSING = "Processing"


class GraphNodeColor(str, Enum):
    """Interactive star graph node color semantic mapping per PRD §8.5"""
    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    GREY = "grey"
    BLUE = "blue"


class ProcessingJobType(str, Enum):
    """Asynchronous job types per PRD §10 and §11.2"""
    INGESTION = "ingestion"
    OCR_EXTRACTION = "ocr_extraction"
    COMPLIANCE_EVALUATION = "compliance_evaluation"
    REPORT_GENERATION = "report_generation"


class ProcessingJobStatus(str, Enum):
    """Asynchronous job execution status per PRD §10"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


# ============================================================================
# Core Entities (PRD §10 & §12.2)
# ============================================================================

class BoundingBox(BaseModel):
    """BoundingBox coordinate contract per PRD §12.3"""
    model_config = ConfigDict(populate_by_name=True)

    page_number: int = Field(..., alias="pageNumber", ge=1, description="1-based document page number")
    page_width: float = Field(..., alias="pageWidth", gt=0, description="Original page width in pixels/points")
    page_height: float = Field(..., alias="pageHeight", gt=0, description="Original page height in pixels/points")
    x1: float = Field(..., description="Top-left X coordinate")
    y1: float = Field(..., description="Top-left Y coordinate")
    x2: float = Field(..., description="Bottom-right X coordinate")
    y2: float = Field(..., description="Bottom-right Y coordinate")


class ComplianceFlag(BaseModel):
    """ComplianceFlag entity per PRD §12.4"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the compliance flag")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    bidder_id: str = Field(..., alias="bidderId", description="Associated Bidder identifier")
    rule_id: Optional[str] = Field(default=None, alias="ruleId", description="Optional associated Tender Rule identifier")
    status: ComplianceFlagStatus = Field(..., description="Compliance status of the finding per PRD §8.4 / §12.4")
    severity: SeverityLevel = Field(..., description="Risk severity level")
    title: str = Field(..., description="Short human-readable summary of the finding")
    reason: str = Field(..., description="Detailed explanation of the contradiction or rule result")
    evidence_ids: List[str] = Field(default_factory=list, alias="evidenceIds", description="Identifiers of linked evidence anchors")
    linked_flag_ids: Optional[List[str]] = Field(default=None, alias="linkedFlagIds", description="Identifiers of related or conflicting compliance flags")
    ai_recommendation: str = Field(..., alias="aiRecommendation", description="Original automated recommendation from the Compliance Engine")
    officer_decision: Optional[str] = Field(default=None, alias="officerDecision", description="Current officer decision state if reviewed")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class OfficerDecision(BaseModel):
    """Officer review decision record on a compliance flag per PRD §9.1 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the decision record")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    bidder_id: str = Field(..., alias="bidderId", description="Associated Bidder identifier")
    flag_id: str = Field(..., alias="flagId", description="Target compliance flag ID")
    decision: OfficerDecisionState = Field(..., description="Officer decision state per PRD §9.1")
    officer_user_id: str = Field(..., alias="officerUserId", description="Identity of the reviewing procurement officer")
    officer_role: str = Field(..., alias="officerRole", description="Role of the officer")
    notes: Optional[str] = Field(default=None, description="Officer rationale or override explanation")
    previous_decision_state: Optional[OfficerDecisionState] = Field(
        default=None,
        alias="previousDecisionState",
        description="Previous decision state prior to this action",
    )
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp when decision was made")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class AuditEvent(BaseModel):
    """
    Immutable append-only audit event per PRD §9.2 and §10.
    Frozen to enforce immutability across the system.
    """
    model_config = ConfigDict(populate_by_name=True, frozen=True)

    id: str = Field(..., description="Audit Event ID")
    tender_id: str = Field(..., alias="tenderId", description="Tender ID")
    bidder_id: str = Field(..., alias="bidderId", description="Bidder ID")
    document_id: Optional[str] = Field(default=None, alias="documentId", description="Document ID, where applicable")
    compliance_flag_id: Optional[str] = Field(default=None, alias="complianceFlagId", description="Compliance Flag ID, where applicable")
    officer_user_id: str = Field(..., alias="officerUserId", description="Officer User ID")
    officer_role: str = Field(..., alias="officerRole", description="Officer Role")
    ai_recommendation: str = Field(..., alias="aiRecommendation", description="Original AI Recommendation")
    officer_decision: str = Field(..., alias="officerDecision", description="Officer Decision")
    officer_notes: Optional[str] = Field(default=None, alias="officerNotes", description="Officer Notes")
    timestamp: str = Field(..., description="Timestamp of the action")
    previous_decision_state: Optional[str] = Field(default=None, alias="previousDecisionState", description="Previous Decision State")
    new_decision_state: str = Field(..., alias="newDecisionState", description="New Decision State")


class Tender(BaseModel):
    """Tender procurement opportunity and workspace per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the tender")
    tender_number: str = Field(..., alias="tenderNumber", description="Official tender reference number / code")
    title: str = Field(..., description="Tender title")
    description: Optional[str] = Field(default=None, description="Detailed description of the tender")
    status: str = Field(..., description="Status of the tender workspace (e.g. draft, active, evaluating, completed, archived)")
    closing_date: Optional[str] = Field(default=None, alias="closingDate", description="Tender submission deadline")
    created_by_id: Optional[str] = Field(default=None, alias="createdById", description="User identifier who created the tender")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class TenderRule(BaseModel):
    """Tender-specific compliance rule definition per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the tender rule")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    rule_code: str = Field(..., alias="ruleCode", description="Unique rule code (e.g. GSTIN_MATCH, TURNOVER_THRESHOLD, LEGAL_NAME_MATCH)")
    name: str = Field(..., description="Display name of the rule")
    description: str = Field(..., description="Detailed explanation of what the rule validates")
    rule_type: str = Field(..., alias="ruleType", description="Category of rule (e.g. threshold, cross_match, presence, validity)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary rule-specific configuration parameters and thresholds")
    severity: SeverityLevel = Field(..., description="Default severity when this rule is violated")
    is_required: bool = Field(default=True, alias="isRequired", description="Whether passing this rule is mandatory for compliance")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class RequiredDocument(BaseModel):
    """Required document definition attached to a tender per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the required document rule")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    document_type: str = Field(..., alias="documentType", description="Canonical document category")
    display_name: str = Field(..., alias="displayName", description="User-facing label for the document requirement")
    description: Optional[str] = Field(default=None, description="Guidelines or expectations for this document")
    is_required: bool = Field(default=True, alias="isRequired", description="Whether document submission is mandatory")
    allowed_extensions: List[str] = Field(default_factory=list, alias="allowedExtensions", description="Permitted file extensions")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class Bidder(BaseModel):
    """Bidder entity submitting a bid package per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the bidder")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    name: str = Field(..., description="Legal entity name of the bidder")
    registration_number: Optional[str] = Field(default=None, alias="registrationNumber", description="Corporate registration or incorporation number")
    gstin: Optional[str] = Field(default=None, description="Primary GST identification number")
    pan: Optional[str] = Field(default=None, description="Permanent Account Number")
    udyam_number: Optional[str] = Field(default=None, alias="udyamNumber", description="MSME / Udyam registration number")
    status: str = Field(..., description="Current processing or compliance state")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class Document(BaseModel):
    """Uploaded bidder document record per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the document")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    bidder_id: str = Field(..., alias="bidderId", description="Associated Bidder identifier")
    required_document_id: Optional[str] = Field(default=None, alias="requiredDocumentId", description="Optional identifier of the matched tender requirement")
    document_type: Optional[str] = Field(default=None, alias="documentType", description="Classified document type")
    file_name: str = Field(..., alias="fileName", description="Original file name of the upload")
    file_size: int = Field(..., alias="fileSize", ge=0, description="Size in bytes")
    file_type: str = Field(..., alias="fileType", description="MIME type or file extension")
    storage_path: str = Field(..., alias="storagePath", description="MinIO / S3 object storage key path")
    page_count: int = Field(default=0, alias="pageCount", ge=0, description="Number of pages")
    status: str = Field(..., description="Processing status (e.g. uploaded, processing, preprocessed, extracted, evaluated, failed)")
    error_message: Optional[str] = Field(default=None, alias="errorMessage", description="Error details if processing failed")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last update")


class DocumentPage(BaseModel):
    """Document page in a multipage document per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the document page")
    document_id: str = Field(..., alias="documentId", description="Associated Document identifier")
    page_number: int = Field(..., alias="pageNumber", ge=1, description="1-based page number")
    page_width: float = Field(..., alias="pageWidth", gt=0, description="Page width in coordinate space points")
    page_height: float = Field(..., alias="pageHeight", gt=0, description="Page height in coordinate space points")
    image_storage_path: Optional[str] = Field(default=None, alias="imageStoragePath", description="Object storage path for pre-rendered page image")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")


class ProcessingJob(BaseModel):
    """Asynchronous job tracking state per PRD §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the processing job")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    bidder_id: Optional[str] = Field(default=None, alias="bidderId", description="Optional associated Bidder identifier")
    document_id: Optional[str] = Field(default=None, alias="documentId", description="Optional associated Document identifier")
    job_type: ProcessingJobType = Field(..., alias="jobType", description="Type of asynchronous task")
    status: ProcessingJobStatus = Field(..., description="Current lifecycle status of the job")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Percentage progress from 0 to 100")
    current_step: Optional[str] = Field(default=None, alias="currentStep", description="Human-readable label of current processing stage")
    error_message: Optional[str] = Field(default=None, alias="errorMessage", description="Error details if job failed")
    retry_count: int = Field(default=0, alias="retryCount", ge=0, description="Number of retries attempted")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of job creation")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of last status update")
    completed_at: Optional[str] = Field(default=None, alias="completedAt", description="ISO 8601 timestamp when job finished")


class ExtractedField(BaseModel):
    """Extracted OCR and Layout-aware field per PRD §8.3 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the extracted field")
    document_id: str = Field(..., alias="documentId", description="Associated Document identifier")
    page_number: int = Field(..., alias="pageNumber", ge=1, description="1-based document page number")
    field_name: str = Field(..., alias="fieldName", description="Canonical field identifier")
    raw_text: str = Field(..., alias="rawText", description="Unmodified text detected by OCR")
    normalized_value: Optional[Any] = Field(default=None, alias="normalizedValue", description="Parsed and typed value")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence score between 0.0 and 1.0")
    bounding_box: BoundingBox = Field(..., alias="boundingBox", description="Bounding box coordinates on the document page per PRD §12.3")
    extraction_method: str = Field(..., alias="extractionMethod", description="Model or pipeline used")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of extraction")


class EvidenceAnchor(BaseModel):
    """Visual evidence coordinate anchor linking findings to page canvas per PRD §8.6 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the evidence anchor")
    document_id: str = Field(..., alias="documentId", description="Associated Document identifier")
    page_number: int = Field(..., alias="pageNumber", ge=1, description="Target page number")
    bounding_box: BoundingBox = Field(..., alias="boundingBox", description="Bounding box coordinates on the page canvas per PRD §12.3")
    extracted_field_id: Optional[str] = Field(default=None, alias="extractedFieldId", description="Optional associated ExtractedField ID")
    compliance_flag_id: Optional[str] = Field(default=None, alias="complianceFlagId", description="Optional associated ComplianceFlag ID")
    highlight_color: Optional[HighlightColor] = Field(default=None, alias="highlightColor", description="Highlight overlay color per PRD §8.6")
    label: Optional[str] = Field(default=None, description="Short badge text displayed on hover/click")
    snippet: Optional[str] = Field(default=None, description="Text snippet extracted inside this bounding region")
    created_at: str = Field(..., alias="createdAt", description="ISO 8601 timestamp of creation")


class GraphNodePosition(BaseModel):
    """Position coordinates for interactive graph nodes"""
    model_config = ConfigDict(populate_by_name=True)

    x: float
    y: float


class GraphNode(BaseModel):
    """Interactive star graph node representation per PRD §8.5 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the node")
    type: Literal["bidder", "document"] = Field(..., description="Node category in the star topology")
    label: str = Field(..., description="Display label on the node")
    status: GraphNodeStatus = Field(..., description="Compliance and processing status determining color per PRD §8.5")
    color: GraphNodeColor = Field(..., description="Assigned node status color per PRD §8.5")
    data: Dict[str, Any] = Field(default_factory=dict, description="Metadata payload including document ID, flag count, and status flags")
    position: Optional[GraphNodePosition] = Field(default=None, description="Optional 2D coordinate position for React Flow canvas")


class GraphEdge(BaseModel):
    """Interactive star graph edge representation per PRD §8.5 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Unique identifier for the edge")
    source: str = Field(..., description="Source node identifier")
    target: str = Field(..., description="Target node identifier")
    type: Optional[str] = Field(default=None, description="Edge render type (e.g. radial, contradiction, smoothstep)")
    label: Optional[str] = Field(default=None, description="Optional label rendered along the edge")
    animated: Optional[bool] = Field(default=False, description="Whether the edge displays animation")
    style: Optional[Dict[str, Any]] = Field(default=None, description="Optional CSS / styling overrides")


class BidderComplianceSummary(BaseModel):
    """Aggregated bidder compliance score and risk summary per PRD §8.1 and §10"""
    model_config = ConfigDict(populate_by_name=True)

    bidder_id: str = Field(..., alias="bidderId", description="Associated Bidder identifier")
    tender_id: str = Field(..., alias="tenderId", description="Associated Tender identifier")
    bidder_name: str = Field(..., alias="bidderName", description="Legal entity name of the bidder")
    compliance_score: float = Field(..., alias="complianceScore", ge=0.0, le=100.0, description="Calculated compliance score percentage (0-100)")
    total_documents: int = Field(default=0, alias="totalDocuments", ge=0, description="Total required documents count")
    submitted_documents: int = Field(default=0, alias="submittedDocuments", ge=0, description="Count of documents successfully submitted and verified")
    missing_documents: int = Field(default=0, alias="missingDocuments", ge=0, description="Count of missing mandatory documents")
    verified_flags_count: int = Field(default=0, alias="verifiedFlagsCount", ge=0, description="Count of Verified compliance flags")
    needs_review_flags_count: int = Field(default=0, alias="needsReviewFlagsCount", ge=0, description="Count of Needs Review or low-confidence flags")
    non_compliance_flags_count: int = Field(default=0, alias="nonComplianceFlagsCount", ge=0, description="Count of Potential/Confirmed Non-Compliance flags")
    confirmed_flags_count: int = Field(default=0, alias="confirmedFlagsCount", ge=0, description="Count of flags confirmed by officer")
    unresolved_flags_count: int = Field(default=0, alias="unresolvedFlagsCount", ge=0, description="Count of pending flags awaiting officer review")
    processing_status: str = Field(..., alias="processingStatus", description="Aggregate processing state")
    primary_risk_reasons: List[str] = Field(default_factory=list, alias="primaryRiskReasons", description="Summary bullet points of highest severity findings")
    overall_status: str = Field(..., alias="overallStatus", description="Tender dashboard status category")
    updated_at: str = Field(..., alias="updatedAt", description="ISO 8601 timestamp of summary generation")
