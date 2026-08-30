/**
 * GovFlow Shared Types — TypeScript Definitions
 * Authoritative shared types matching GovFlow_PRD.md §10, §12, §8, and §9.
 */

// ============================================================================
// Enums & Primitive Unions
// ============================================================================

/**
 * Compliance flag status union per PRD §8.4 and §12.4
 */
export type ComplianceFlagStatus =
  | "Verified"
  | "Potential Non-Compliance"
  | "Needs Review"
  | "Insufficient Evidence"
  | "Missing";

/**
 * Finding risk severity level per PRD §12.4
 */
export type SeverityLevel = "low" | "medium" | "high" | "critical";

/**
 * Officer decision states per PRD §9.1
 */
export type OfficerDecisionState =
  | "Pending"
  | "Confirmed"
  | "Rejected"
  | "Overridden"
  | "Escalated";

/**
 * Visual evidence highlight overlay colors per PRD §8.6
 */
export type HighlightColor = "red" | "amber" | "green" | "blue";

/**
 * Interactive star graph node status per PRD §8.5
 */
export type GraphNodeStatus =
  | "Verified"
  | "Potential Non-Compliance"
  | "Confirmed Non-Compliance"
  | "Needs Review"
  | "Insufficient Evidence"
  | "Missing"
  | "Processing";

/**
 * Interactive star graph node color semantic mapping per PRD §8.5
 */
export type GraphNodeColor = "green" | "amber" | "red" | "grey" | "blue";

/**
 * Asynchronous job types per PRD §10 and §11.2
 */
export type ProcessingJobType =
  | "ingestion"
  | "ocr_extraction"
  | "compliance_evaluation"
  | "report_generation";

/**
 * Asynchronous job execution status per PRD §10
 */
export type ProcessingJobStatus =
  | "queued"
  | "processing"
  | "completed"
  | "failed"
  | "retrying";

// ============================================================================
// Core Entities (PRD §10 & §12.2)
// ============================================================================

/**
 * BoundingBox coordinate contract per PRD §12.3
 */
export interface BoundingBox {
  pageNumber: number;
  pageWidth: number;
  pageHeight: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

/**
 * ComplianceFlag entity per PRD §12.4
 */
export interface ComplianceFlag {
  id: string;
  tenderId: string;
  bidderId: string;
  ruleId?: string;
  status: ComplianceFlagStatus;
  severity: SeverityLevel;
  title: string;
  reason: string;
  evidenceIds: string[];
  linkedFlagIds?: string[];
  aiRecommendation: string;
  officerDecision?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Officer review decision record on a compliance flag per PRD §9.1 and §10
 */
export interface OfficerDecision {
  id: string;
  tenderId: string;
  bidderId: string;
  flagId: string;
  decision: OfficerDecisionState;
  officerUserId: string;
  officerRole: string;
  notes?: string;
  previousDecisionState?: OfficerDecisionState;
  createdAt: string;
  updatedAt: string;
}

/**
 * Immutable append-only audit event per PRD §9.2 and §10
 */
export interface AuditEvent {
  readonly id: string;
  readonly tenderId: string;
  readonly bidderId: string;
  readonly documentId?: string;
  readonly complianceFlagId?: string;
  readonly officerUserId: string;
  readonly officerRole: string;
  readonly aiRecommendation: string;
  readonly officerDecision: OfficerDecisionState | string;
  readonly officerNotes?: string;
  readonly timestamp: string;
  readonly previousDecisionState?: OfficerDecisionState | string;
  readonly newDecisionState: OfficerDecisionState | string;
}

/**
 * Tender procurement opportunity and workspace per PRD §10
 */
export interface Tender {
  id: string;
  tenderNumber: string;
  title: string;
  description?: string;
  status: "draft" | "active" | "evaluating" | "completed" | "archived" | string;
  closingDate?: string;
  createdById?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Tender-specific compliance rule definition per PRD §10
 */
export interface TenderRule {
  id: string;
  tenderId: string;
  ruleCode: string;
  name: string;
  description: string;
  ruleType: "threshold" | "cross_match" | "presence" | "validity" | string;
  parameters: Record<string, any>;
  severity: SeverityLevel;
  isRequired: boolean;
  createdAt: string;
  updatedAt: string;
}

/**
 * Required document definition attached to a tender per PRD §10
 */
export interface RequiredDocument {
  id: string;
  tenderId: string;
  documentType: string;
  displayName: string;
  description?: string;
  isRequired: boolean;
  allowedExtensions: string[];
  createdAt: string;
  updatedAt: string;
}

/**
 * Bidder entity submitting a bid package per PRD §10
 */
export interface Bidder {
  id: string;
  tenderId: string;
  name: string;
  registrationNumber?: string;
  gstin?: string;
  pan?: string;
  udyamNumber?: string;
  status:
    | "submitted"
    | "processing"
    | "evaluated"
    | "compliant"
    | "needs_review"
    | "non_compliant"
    | string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Uploaded bidder document record per PRD §10
 */
export interface Document {
  id: string;
  tenderId: string;
  bidderId: string;
  requiredDocumentId?: string;
  documentType?: string;
  fileName: string;
  fileSize: number;
  fileType: string;
  storagePath: string;
  pageCount: number;
  status:
    | "uploaded"
    | "processing"
    | "preprocessed"
    | "extracted"
    | "evaluated"
    | "failed"
    | string;
  errorMessage?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Document page in a multipage document per PRD §10
 */
export interface DocumentPage {
  id: string;
  documentId: string;
  pageNumber: number;
  pageWidth: number;
  pageHeight: number;
  imageStoragePath?: string;
  createdAt: string;
}

/**
 * Asynchronous job tracking state per PRD §10
 */
export interface ProcessingJob {
  id: string;
  tenderId: string;
  bidderId?: string;
  documentId?: string;
  jobType: ProcessingJobType;
  status: ProcessingJobStatus;
  progress: number;
  currentStep?: string;
  errorMessage?: string;
  retryCount: number;
  createdAt: string;
  updatedAt: string;
  completedAt?: string;
}

/**
 * Extracted OCR and Layout-aware field per PRD §8.3 and §10
 */
export interface ExtractedField {
  id: string;
  documentId: string;
  pageNumber: number;
  fieldName: string;
  rawText: string;
  normalizedValue?: any;
  confidence: number;
  boundingBox: BoundingBox;
  extractionMethod:
    | "paddle_ocr"
    | "layoutlmv3"
    | "rule_based"
    | "hybrid"
    | string;
  createdAt: string;
}

/**
 * Visual evidence coordinate anchor linking findings to page canvas per PRD §8.6 and §10
 */
export interface EvidenceAnchor {
  id: string;
  documentId: string;
  pageNumber: number;
  boundingBox: BoundingBox;
  extractedFieldId?: string;
  complianceFlagId?: string;
  highlightColor?: HighlightColor;
  label?: string;
  snippet?: string;
  createdAt: string;
}

/**
 * Position coordinates for interactive graph nodes
 */
export interface GraphNodePosition {
  x: number;
  y: number;
}

/**
 * Interactive star graph node representation per PRD §8.5 and §10
 */
export interface GraphNode {
  id: string;
  type: "bidder" | "document";
  label: string;
  status: GraphNodeStatus;
  color: GraphNodeColor;
  data: Record<string, any>;
  position?: GraphNodePosition;
}

/**
 * Interactive star graph edge representation per PRD §8.5 and §10
 */
export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type?: "radial" | "contradiction" | "default" | string;
  label?: string;
  animated?: boolean;
  style?: Record<string, any>;
}

/**
 * Aggregated bidder compliance score and risk summary per PRD §8.1 and §10
 */
export interface BidderComplianceSummary {
  bidderId: string;
  tenderId: string;
  bidderName: string;
  complianceScore: number;
  totalDocuments: number;
  submittedDocuments: number;
  missingDocuments: number;
  verifiedFlagsCount: number;
  needsReviewFlagsCount: number;
  nonComplianceFlagsCount: number;
  confirmedFlagsCount: number;
  unresolvedFlagsCount: number;
  processingStatus: "pending" | "processing" | "completed" | "failed" | string;
  primaryRiskReasons: string[];
  overallStatus:
    | "Compliant"
    | "Needs Review"
    | "Non-Compliant"
    | "Missing Documents"
    | "Processing"
    | string;
  updatedAt: string;
}
