# GovFlow — Product Requirements Document

**Project:** GovFlow
**Version:** 1.1
**Status:** Approved for Development
**Last Updated:** 30-08-2026

---

## 1. Project Summary

GovFlow is an interactive audit and compliance platform designed for procurement officers evaluating tender bid packages.

It replaces manual, disconnected document verification with an automated, visually navigable, evidence-first workflow. GovFlow extracts intelligence from submitted bid documents, identifies compliance gaps and contradictions, and presents every finding alongside its original visual evidence.

The platform supports faster, more accurate, defensible tender evaluations while preserving human authority over all final compliance decisions.

GovFlow does not autonomously reject bidders. It provides recommendations, evidence, and audit trails for officer review.

---

## 2. Problem Statement

Procurement officers must evaluate complex bidder packages containing multiple documents such as:

- GST certificates
- Udyam certificates
- CA certificates
- Financial statements
- Turnover declarations
- Registration documents
- Tender-specific compliance documents

The current manual process requires officers to open many files, verify details individually, and cross-reference values between documents.

This process is:

- **Slow:** Officers manually review dozens of documents for every bidder.
- **Error-prone:** Repetitive cross-checking can result in missed inconsistencies.
- **Untraceable:** Manual decisions may not clearly reference the exact source evidence.
- **Difficult to prioritize:** Officers cannot immediately identify high-risk bidders.
- **Low trust in opaque AI:** Traditional automated scores often lack visual proof or source traceability.

GovFlow solves this by connecting every compliance recommendation directly to extracted data, document pages, and visual bounding-box evidence.

---

## 3. Product Vision

GovFlow will become a trusted tender compliance workspace where procurement officers can:

1. Upload and process complete bidder packages.
2. Automatically extract important compliance fields.
3. Detect missing documents, contradictions, low-confidence fields, and rule violations.
4. Review bidder risk through a tender-level dashboard.
5. Explore bidder documents through an interactive star topology graph.
6. Inspect original source documents with visual evidence overlays.
7. Confirm, reject, or override AI recommendations.
8. Generate a complete explainable compliance report and audit trail.

---

## 4. Goals and Success Criteria

| **Goal** | **Success Metric**          |                                                                                                                           |
| --- | --- | ------------------------------------------------------------------------------------------------------------------------- |
| Reduce manual cross-referencing | Officer review time per bidder is significantly lower than the manual baseline                                            |
| Improve trust in automation     | Every AI-generated flag is linked to at least one source document and bounding box                                        |
| Improve compliance accuracy     | Cross-document contradictions and missing documents are correctly identified                                              |
| Enable rapid prioritization     | Officers can identify high-risk bidders from the dashboard within seconds                                                 |
| Preserve officer authority      | No bidder is automatically rejected without an officer decision                                                           |
| Maintain auditability           | Every officer action is stored with timestamp, reason, user identity, and original AI recommendation                      |
| Maintain consistent app flow    | Tender, bidder, document, and evidence context persist while navigating across dashboard, graph, viewer, and report pages |

---

## 5. Target Users

### 5.1 Primary Users

**Procurement / Tender Evaluation Officers**

Responsibilities:

- Upload bid packages.
- Review bidder compliance status.
- Verify document evidence.
- Confirm or reject AI-generated findings.
- Produce compliance reports.

### 5.2 Secondary Users

**Compliance Auditors**

Responsibilities:

- Review officer decisions.
- Validate evidence trails.
- Verify policy compliance.

**Tender Committee Members**

Responsibilities:

- Review bidder summaries.
- Compare compliance outcomes.
- Review final audit reports.

---

## 6. Core Product Principles

### 6.1 Evidence-First Decisions

Every automated finding must have traceable evidence. A finding without a document source, page reference, field value, and bounding box must not be displayed as a final compliance recommendation.

### 6.2 Human-in-the-Loop Review

GovFlow provides recommendations only. Procurement officers retain final authority to confirm, reject, or override findings.

### 6.3 Consistent Navigation Context

The active tender, bidder, document, selected flag, and page must remain available when navigating between:

```
Tender Dashboard
   → Bidder Evidence Graph
      → Document Evidence Viewer
         → Officer Decision
            → Compliance Report
```

### 6.4 Independent but Integrated Modules

Every MVP feature must be independently testable, deployable, and maintainable while integrating through shared contracts, events, and common data models.

### 6.5 Contract-First Development

Frontend, API Gateway, AI workers, and reporting modules must use common versioned schemas. No module may rely on undocumented payloads or duplicate business definitions.

---

## 7. User Journey

### 7.1 Tender Setup

1. Officer creates or selects a tender.
2. Officer configures the tender requirements.
3. Required document types and compliance rules are attached to the tender.
4. GovFlow creates the tender workspace.

### 7.2 Bid Package Upload

1. Officer uploads ZIP archives, PDFs, scanned images, or individual documents.
2. GovFlow validates file type, size, format, and tender association.
3. Files are securely stored in object storage.
4. An asynchronous processing job is created.
5. The dashboard displays processing status without blocking the officer.

### 7.3 Processing and Intelligence

1. Files are split into pages where necessary.
2. Images are preprocessed.
3. OCR extracts text and layout-aware field coordinates.
4. Documents are classified by type.
5. Extracted fields are normalized.
6. The compliance engine applies tender rules.
7. Contradictions, missing documents, low-confidence fields, and rule violations are generated.
8. The dashboard, graph, and viewer receive updated status data.

### 7.4 Bidder Review

1. Officer opens the tender dashboard.
2. Officer identifies bidders with the highest risk or most missing documents.
3. Officer selects a bidder.
4. GovFlow opens the Bidder Evidence Graph.
5. Officer selects a document node or flag.
6. GovFlow opens the exact document page and highlights the source evidence.
7. Officer confirms, rejects, or overrides the recommendation.

### 7.5 Report Generation

1. Officer opens the bidder report.
2. GovFlow compiles AI findings, evidence links, and officer actions.
3. Officer reviews the final report.
4. The report is generated for viewing or download.
5. A final immutable audit record is stored.

---

## 8. MVP Features

Each feature is an independent module with defined inputs, outputs, events, data contracts, and test coverage.

---

### 8.1 Tender-Level Bidder Dashboard

**Feature ID:** **`F-01`**

**Input:** Tender ID

**Output:**

- Aggregated bidder list
- Bidder compliance score
- Document counts
- Missing document count
- Confirmed and unresolved flags
- Processing status
- Primary risk reasons

**Functionality:**

- Displays all bidders participating in the selected tender.
- Sorts bidders by compliance risk, missing documents, or processing status.
- Allows officers to open a bidder graph or report.
- Shows live processing updates where available.
- Supports filters for compliant, needs-review, non-compliant, missing, and processing bidders.

**Primary Component:**

```
BidderListDashboard
```

**Acceptance Criteria:**

- The dashboard loads bidder data for the active tender.
- Every bidder shows current document and compliance status.
- Clicking a bidder opens the correct bidder graph.
- Dashboard status updates after processing events complete.
- Tender context remains persistent on refresh and navigation.

---

### 8.2 Batch Bid-Package Upload and Ingestion

**Feature ID:** **`F-02`**

**Input:**

- ZIP archive
- PDF files
- Image files
- Tender ID
- Optional bidder association metadata

**Output:**

- Secure object storage references
- Processing job ID
- Structured bidder-document records
- Upload status
- Ingestion events

**Functionality:**

- Validates file type and upload constraints.
- Stores originals securely.
- Extracts ZIP contents where applicable.
- Splits multipage PDFs into processable page records.
- Converts and preprocesses scanned images.
- Associates documents with tender and bidder records.
- Publishes ingestion events to the queue.

**Supported MVP File Types:**

```
.pdf
.png
.jpg
.jpeg
.zip
```

**Primary Components:**

```
UploadDropzone
UploadProgress
```

**Acceptance Criteria:**

- Invalid file types are rejected before processing.
- Valid uploads create a document record and processing job.
- Original documents are stored without modification.
- Each uploaded file is linked to a tender and bidder context.
- Upload completion triggers an asynchronous processing event.
- Officers can see real-time or polling-based upload status.

---

### 8.3 OCR and Layout-Aware Field Extraction

**Feature ID:** **`F-03`**

**Input:**

- Preprocessed document image
- PDF page image
- Document metadata
- Page dimensions

**Output:**

- Extracted text
- Identified fields
- Normalized field values
- Bounding-box coordinates
- Page number
- OCR confidence score
- Extraction metadata

**Example Extracted Fields:**

```
GSTIN
Udyam Registration Number
Legal Entity Name
Registered Address
Turnover Value
Financial Year
Certificate Date
PAN
Authorized Signatory
Document Number
```

**Functionality:**

- Uses PaddleOCR for OCR extraction.
- Uses LayoutLMv3 for spatial and layout-aware field interpretation.
- Preserves original page coordinates.
- Captures extraction confidence for every field.
- Stores results in a normalized document extraction format.
- Provides data required by the Evidence Viewer and Compliance Engine.

**Bounding Box Format:**

```
{
  "pageNumber": 1,
  "pageWidth": 2480,
  "pageHeight": 3508,
  "boundingBox": [x1, y1, x2, y2]
}
```

**Acceptance Criteria:**

- Every extracted field includes source document ID and page number.
- Every visualizable field includes page dimensions and bounding-box coordinates.
- OCR confidence is stored for each extracted value.
- Extraction results are available to the compliance engine through shared schemas.
- Low-confidence fields can be shown in the Evidence Viewer.

---

### 8.4 Contradiction, Clarity, and Uncertainty Engine

**Feature ID:** **`F-04`**

**Input:**

- Extracted field JSON payloads
- Document metadata
- Tender rules
- Required document definitions
- OCR confidence data
- Bidder package context

**Output:**

- Compliance flags
- Rule evaluation results
- Evidence links
- Cross-document contradiction links
- Bidder compliance summary

**Rule Status Values:**

| ****Meaning**             ** |                                                                             |
| --- | --- | --------------------------------------------------------------------------- |
| **`Verified`**                 | Required value or rule is satisfied with sufficient evidence                |
| **`Potential Non-Compliance`** | Extracted data indicates a possible rule violation or contradiction         |
| **`Needs Review`**             | A finding requires officer review, often due to ambiguity or low confidence |
| **`Insufficient Evidence`**    | Data is unavailable, unclear, incomplete, or unreliable                     |
| **`Missing`**                  | A required document or field is not available                               |

**Functionality:**

- Compares GSTINs across multiple documents.
- Compares bidder legal names across documents.
- Compares addresses across documents.
- Validates turnover thresholds against tender rules.
- Detects missing required documents.
- Detects conflicting dates, registration numbers, and entity information.
- Distinguishes probable non-compliance from low-confidence OCR extraction.
- Creates evidence links between conflicting values.

**Example Contradiction:**

```
GST Certificate GSTIN: 27ABCDE1234F1Z5
CA Certificate GSTIN: 29ABCDE1234F1Z5

Result:
Potential Non-Compliance
Reason:
GSTIN mismatch between GST Certificate and CA Certificate
Evidence:
Bounding boxes from both source documents
```

**Acceptance Criteria:**

- Every generated flag references a tender rule or document requirement.
- Every contradiction references all involved source fields.
- Every evidence-backed flag includes document ID, page number, and bounding box.
- Low-confidence extraction is not automatically treated as confirmed non-compliance.
- Missing required documents generate **`Missing`** status flags.
- Officer overrides never delete original AI findings.

---

### 8.5 Interactive Bidder-Document Star Graph

**Feature ID:** **`F-05`**

**Input:**

- Bidder metadata
- Document metadata
- Compliance flags
- Required document configuration
- Processing status

**Output:**

- Interactive star topology visualization
- Document nodes
- Rule status indicators
- Node details panel
- Navigation events to document evidence

**Functionality:**

- Displays the selected bidder as the central node.
- Displays submitted and required documents as surrounding nodes.
- Displays document state using consistent color semantics.
- Supports selection of nodes and related flags.
- Opens document context in the Evidence Viewer.
- Displays extracted attributes, flags, confidence values, and linked evidence.

**Primary Component:**

```
BidderStarGraph
```

**Node Color Rules:**

| **Color** | ****Meaning**** |                                                     |                                                                                 |
| --- | --- | --- |
| Green                  | Verified                                            | Document is present and checks appear compliant                                 |
| Amber                  | Needs Review / Insufficient Evidence                | Document is present but requires officer review or extraction confidence is low |
| Red                    | Potential Non-Compliance / Confirmed Non-Compliance | A contradiction or rule violation has been detected or confirmed                |
| Grey                   | Missing                                             | Required document is missing                                                    |
| Blue                   | Processing                                          | Document is uploaded but processing or verification is incomplete               |

**Status Priority for Node Coloring:**

```
Processing → Blue
Missing → Grey
Potential/Confirmed Non-Compliance → Red
Needs Review / Insufficient Evidence → Amber
Verified → Green
```

**Acceptance Criteria:**

- The bidder is displayed as the central graph node.
- Required and uploaded documents appear as connected document nodes.
- Node colors match current compliance and processing status.
- Selecting a node opens document details and relevant flags.
- Selecting evidence opens the exact document in the Evidence Viewer.
- Graph state remains consistent after browser navigation or page refresh.

---

### 8.6 In-Document Evidence Viewer

**Feature ID:** **`F-06`**

**Input:**

- Original PDF or image
- Page metadata
- Extracted field coordinates
- Compliance flags
- Linked conflicting evidence
- Display canvas dimensions

**Output:**

- Rendered PDF or image page
- Scaled visual bounding-box overlays
- Evidence side panel
- Linked document navigation

**Functionality:**

- Renders PDF pages or image documents.
- Scales original page coordinates to the rendered canvas.
- Displays visual overlays for extracted fields and anomalies.
- Allows officers to click evidence boxes.
- Displays the associated rule, extracted value, confidence score, and source details.
- Navigates to linked evidence in conflicting documents.

**Primary Component:**

```
EvidenceDocumentViewer
```

**Highlight Color Rules:**

| **Highlight** | **Meaning** |                                                           |
| -------------------- | --------------------------------------------------------- |
| Red                  | Compliance violation, contradiction, or confirmed risk    |
| Amber                | Low-confidence extraction, unclear value, or needs review |
| Green                | Verified supporting evidence                              |
| Blue                 | Currently selected evidence or active document context    |

**Acceptance Criteria:**

- Bounding boxes align accurately with the original document content.
- The viewer can render at different screen sizes without losing coordinate accuracy.
- Clicking an anomaly opens relevant evidence details.
- Contradiction findings link to the conflicting source document.
- Officers can navigate between document pages and evidence sources.
- Page, document, bidder, and tender context remain persistent.

---

### 8.7 Explainable Officer Report

**Feature ID:** **`F-07`**

**Input:**

- Tender metadata
- Bidder metadata
- Compliance flags
- Source evidence references
- Officer decisions
- Audit logs
- Compliance summary

**Output:**

- Viewable report
- Downloadable compliance report
- Officer decision history
- Evidence audit trail

**Functionality:**

- Generates a bidder-level compliance report.
- Shows AI recommendations and officer outcomes separately.
- Includes evidence references for every significant finding.
- Includes decision timestamps, officer identity, notes, and overrides.
- Supports report generation after review completion.

**Primary Components:**

```
ReportViewer
DecisionLogTable
```

**Acceptance Criteria:**

- Reports include bidder identity and tender context.
- Reports show all AI flags and final officer decisions.
- Reports include source document and page references.
- Officer overrides are explicitly visible.
- Reports can be viewed and downloaded.
- Generated reports preserve audit integrity and cannot silently overwrite past decisions.

---

## 9. Officer Decisions and Audit Trail

### 9.1 Officer Decision States

| **Decision** | **Meaning** |                                                       |
| ------------------- | ----------------------------------------------------- |
| **`Pending`**       | No officer action has been taken                      |
| **`Confirmed`**     | Officer confirms the AI recommendation                |
| **`Rejected`**      | Officer rejects the AI recommendation                 |
| **`Overridden`**    | Officer provides an alternative decision or rationale |
| **`Escalated`**     | Officer forwards the finding for secondary review     |

### 9.2 Audit Log Requirements

Every officer action must create an audit event containing:

```
Audit Event ID
Tender ID
Bidder ID
Document ID, where applicable
Compliance Flag ID, where applicable
Officer User ID
Officer Role
AI Recommendation
Officer Decision
Officer Notes
Timestamp
Previous Decision State
New Decision State
```

Audit records must be append-only. Existing recommendations and prior officer decisions must remain visible.

---

## 10. Core Data Entities

| **Entity** | **Purpose**             |                                                                    |
| --- | --- | ------------------------------------------------------------------ |
| **`Tender`**                  | Represents a procurement opportunity and its evaluation workspace  |
| **`TenderRule`**              | Defines tender-specific compliance requirements                    |
| **`RequiredDocument`**        | Defines required document types for a tender                       |
| **`Bidder`**                  | Represents a company submitting a bid package                      |
| **`Document`**                | Represents an uploaded bidder document                             |
| **`DocumentPage`**            | Represents a page in a multipage document                          |
| **`ProcessingJob`**           | Tracks ingestion, OCR, extraction, and compliance processing state |
| **`ExtractedField`**          | Stores extracted field values, confidence, and coordinates         |
| **`EvidenceAnchor`**          | Connects a field or flag to document page coordinates              |
| **`ComplianceFlag`**          | Stores a rule result, severity, status, and evidence               |
| **`OfficerDecision`**         | Stores officer confirmation, rejection, override, or escalation    |
| **`AuditEvent`**              | Stores immutable system and officer activity records               |
| **`BidderComplianceSummary`** | Stores aggregated bidder compliance data for the dashboard         |

---

## 11. Architecture and Technical Design

GovFlow uses an event-driven and decoupled architecture so that OCR and compliance processing do not block the officer interface.

### 11.1 High-Level Architecture

```
graph TD
    Officer["Procurement Officer"]
    Web["GovFlow Web Application"]
    Gateway["API Gateway"]
    Storage["Secure Object Storage"]
    Queue["Queue / Event Bus"]
    IngestionWorker["Ingestion Worker"]
    OCRWorker["OCR and Layout Worker"]
    Engine["Compliance Rules Engine"]
    Database["Operational Database / Graph Repository"]
    Reports["Report Generator"]

    Officer --> Web
    Web <-- REST / GraphQL --> Gateway

    Gateway --> Storage
    Gateway --> Database
    Gateway --> Queue

    Queue --> IngestionWorker
    IngestionWorker --> Storage
    IngestionWorker --> Queue

    Queue --> OCRWorker
    OCRWorker --> Storage
    OCRWorker --> Database
    OCRWorker --> Queue

    Queue --> Engine
    Engine --> Database
    Engine --> Queue

    Gateway --> Reports
    Reports --> Database
    Reports --> Storage
```

### 11.2 Processing Pipeline

1. Officer uploads a bid package.
2. API Gateway validates the request.
3. Original documents are stored in secure object storage.
4. API Gateway creates document and processing job records.
5. API Gateway publishes **`document.uploaded`**.
6. Ingestion Worker preprocesses documents and emits **`document.preprocessed`**.
7. OCR Worker extracts fields, coordinates, and confidence metadata.
8. OCR Worker emits **`document.extraction.completed`**.
9. Compliance Engine evaluates tender rules and cross-document data.
10. Compliance Engine stores flags, evidence links, graph data, and bidder summaries.
11. API Gateway returns updated dashboard, graph, viewer, and report data to the frontend.

### 11.3 Required Events

| **Event** | **Producer** | **Consumer** | **Purpose**      |                   |                         |                                       |
| ------------------------------------- | ----------------- | ----------------------- | ------------------------------------- |
| **`document.uploaded`**               | API Gateway       | Ingestion Worker        | Start ingestion workflow              |
| **`document.preprocessed`**           | Ingestion Worker  | OCR Worker              | Start OCR and layout extraction       |
| **`document.extraction.completed`**   | OCR Worker        | Compliance Engine       | Start compliance evaluation           |
| **`compliance.evaluation.completed`** | Compliance Engine | API Gateway / Dashboard | Refresh bidder summary and graph data |
| **`report.requested`**                | API Gateway       | Report Generator        | Generate a compliance report          |
| **`report.generated`**                | Report Generator  | API Gateway             | Make report available to officer      |

---

## 12. API and Shared Contract Requirements

GovFlow may expose REST APIs, GraphQL APIs, or both. All public payloads must be documented in the shared API contract.

### 12.1 Core API Capabilities

| **Area** | **Example Capability** |                                                              |
| --- | --- | ------------------------------------------------------------ |
| Tenders                    | Create, retrieve, and configure tenders and rules            |
| Bidders                    | Retrieve bidder lists, risk summaries, and compliance status |
| Ingestion                  | Upload documents and retrieve processing status              |
| Documents                  | Retrieve document metadata and secure viewing URLs           |
| Extraction                 | Retrieve extracted fields and confidence data                |
| Compliance                 | Retrieve flags, contradictions, and officer decisions        |
| Graph                      | Retrieve bidder star graph topology                          |
| Evidence                   | Retrieve page coordinates and linked evidence                |
| Reports                    | Generate, view, and download compliance reports              |
| Audit                      | Retrieve officer decision history and audit records          |

### 12.2 Required Shared Types

The following types must be versioned and shared across frontend, API Gateway, AI workers, and report generation:

```
Tender
TenderRule
RequiredDocument
Bidder
Document
DocumentPage
ProcessingJob
ExtractedField
BoundingBox
EvidenceAnchor
ComplianceFlag
OfficerDecision
AuditEvent
GraphNode
GraphEdge
BidderComplianceSummary
```

### 12.3 Bounding Box Contract

```
type BoundingBox = {
  pageNumber: number;
  pageWidth: number;
  pageHeight: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
};
```

### 12.4 Compliance Flag Contract

```
type ComplianceFlagStatus =
  | "Verified"
  | "Potential Non-Compliance"
  | "Needs Review"
  | "Insufficient Evidence"
  | "Missing";

type ComplianceFlag = {
  id: string;
  tenderId: string;
  bidderId: string;
  ruleId?: string;
  status: ComplianceFlagStatus;
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  reason: string;
  evidenceIds: string[];
  linkedFlagIds?: string[];
  aiRecommendation: string;
  officerDecision?: string;
  createdAt: string;
  updatedAt: string;
};
```

---

## 13. Repository and Folder Structure

GovFlow must be maintained as a modular monorepo. This structure keeps independent modules separated while ensuring seamless integration through shared packages and contracts.

```
govflow/
├── apps/
│   ├── web/                     # Frontend visualization layer
│   ├── api-gateway/             # API Gateway, REST/GraphQL delivery, auth
│   └── ai-workers/              # Python workers: ingestion, OCR, compliance, reports
│
├── packages/                    # Shared code and versioned contracts
│   ├── shared-types/
│   ├── api-contracts/
│   ├── ui-kit/
│   └── config/
│
├── infra/                       # Docker, Kubernetes, Terraform, deployment scripts
├── docs/                        # PRD, architecture docs, ADRs
├── .github/
│   └── workflows/               # CI/CD workflows
│
├── turbo.json                   # Monorepo orchestration
├── package.json
└── README.md
```

---

## 14. Frontend Folder Structure

**Location:** **`apps/web/`**

```
apps/web/
├── src/
│   ├── app/
│   │   └── tenders/
│   │       └── [tenderId]/
│   │           ├── dashboard/                    # Tender-Level Bidder Dashboard
│   │           ├── upload/                       # Batch Upload and Ingestion
│   │           └── bidders/
│   │               └── [bidderId]/
│   │                   ├── graph/                # Bidder Star Graph
│   │                   ├── documents/
│   │                   │   └── [documentId]/     # Evidence Document Viewer
│   │                   └── report/               # Officer Report
│   │
│   ├── modules/
│   │   ├── bidder-dashboard/
│   │   │   ├── components/
│   │   │   │   ├── BidderListDashboard.tsx
│   │   │   │   ├── BidderCard.tsx
│   │   │   │   ├── RiskSummary.tsx
│   │   │   │   └── DashboardFilters.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useBidderList.ts
│   │   │   ├── api/
│   │   │   │   └── dashboardApi.ts
│   │   │   └── tests/
│   │   │
│   │   ├── ingestion/
│   │   │   ├── components/
│   │   │   │   ├── UploadDropzone.tsx
│   │   │   │   ├── UploadProgress.tsx
│   │   │   │   └── ProcessingStatus.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useUploadStatus.ts
│   │   │   ├── api/
│   │   │   │   └── ingestionApi.ts
│   │   │   └── tests/
│   │   │
│   │   ├── star-graph/
│   │   │   ├── components/
│   │   │   │   ├── BidderStarGraph.tsx
│   │   │   │   ├── BidderNode.tsx
│   │   │   │   ├── DocumentNode.tsx
│   │   │   │   ├── NodeDetailPanel.tsx
│   │   │   │   └── GraphLegend.tsx
│   │   │   ├── api/
│   │   │   │   └── graphApi.ts
│   │   │   ├── utils/
│   │   │   │   └── nodeColorMap.ts
│   │   │   └── tests/
│   │   │
│   │   ├── evidence-viewer/
│   │   │   ├── components/
│   │   │   │   ├── EvidenceDocumentViewer.tsx
│   │   │   │   ├── DocumentPageCanvas.tsx
│   │   │   │   ├── BoundingBoxOverlay.tsx
│   │   │   │   ├── AnomalySidePanel.tsx
│   │   │   │   └── LinkedEvidencePanel.tsx
│   │   │   ├── api/
│   │   │   │   └── documentApi.ts
│   │   │   ├── utils/
│   │   │   │   └── coordinateScaler.ts
│   │   │   └── tests/
│   │   │
│   │   ├── compliance-flags/
│   │   │   ├── components/
│   │   │   │   ├── FlagBadge.tsx
│   │   │   │   ├── FlagList.tsx
│   │   │   │   ├── OfficerDecisionForm.tsx
│   │   │   │   └── EvidenceReference.tsx
│   │   │   ├── api/
│   │   │   │   └── complianceApi.ts
│   │   │   └── tests/
│   │   │
│   │   └── officer-report/
│   │       ├── components/
│   │       │   ├── ReportViewer.tsx
│   │       │   ├── DecisionLogTable.tsx
│   │       │   └── DownloadReportButton.tsx
│   │       ├── api/
│   │       │   └── reportApi.ts
│   │       └── tests/
│   │
│   ├── shared/
│   │   ├── components/                       # Shared UI components
│   │   ├── constants/
│   │   │   ├── flagStatus.ts
│   │   │   └── nodeStatus.ts
│   │   ├── lib/
│   │   │   ├── apiClient.ts
│   │   │   └── queryClient.ts
│   │   ├── store/
│   │   │   ├── tenderContext.ts
│   │   │   ├── bidderContext.ts
│   │   │   └── evidenceContext.ts
│   │   └── types/
│   │       └── index.ts
│   │
│   └── styles/
│       ├── globals.css
│       └── theme.css
│
├── public/
├── tests/
└── package.json
```

---

## 15. API Gateway Folder Structure

**Location:** **`apps/api-gateway/`**

```
apps/api-gateway/
├── src/
│   ├── modules/
│   │   ├── auth/                   # Authentication, authorization, RBAC
│   │   ├── tenders/                # Tender configuration and tender rules
│   │   ├── bidders/                # Bidder data and dashboard aggregation
│   │   ├── ingestion/              # Upload validation and job creation
│   │   ├── documents/              # Document metadata and secure access URLs
│   │   ├── extraction/             # OCR extraction result delivery
│   │   ├── compliance/             # Compliance flags and officer decisions
│   │   ├── graph/                  # Star graph data aggregation
│   │   ├── evidence/               # Bounding-box and evidence source payloads
│   │   ├── reports/                # Report request and report delivery
│   │   └── audit/                  # Audit log access
│   │
│   ├── events/
│   │   ├── publishers/
│   │   │   ├── documentEvents.ts
│   │   │   ├── processingEvents.ts
│   │   │   └── reportEvents.ts
│   │   └── subscribers/
│   │       ├── extractionCompleted.ts
│   │       ├── complianceCompleted.ts
│   │       └── reportGenerated.ts
│   │
│   ├── database/
│   │   ├── models/
│   │   ├── migrations/
│   │   ├── repositories/
│   │   └── seed/
│   │
│   ├── storage/
│   │   ├── objectStorageAdapter.ts
│   │   └── signedUrlService.ts
│   │
│   ├── common/
│   │   ├── middleware/
│   │   ├── guards/
│   │   ├── filters/
│   │   ├── validators/
│   │   └── utils/
│   │
│   ├── config/
│   └── main.ts
│
├── tests/
└── package.json
```

---

## 16. AI Workers Folder Structure

**Location:** **`apps/ai-workers/`**

```
apps/ai-workers/
├── src/
│   ├── ingestion_worker/
│   │   ├── zip_extractor.py
│   │   ├── pdf_splitter.py
│   │   ├── document_classifier.py
│   │   └── image_preprocessor.py
│   │
│   ├── ocr/
│   │   ├── paddle_ocr_service.py
│   │   ├── layoutlmv3_service.py
│   │   ├── field_normalizer.py
│   │   ├── coordinate_mapper.py
│   │   └── extraction_pipeline.py
│   │
│   ├── compliance_engine/
│   │   ├── rules/
│   │   │   ├── gstin_match.py
│   │   │   ├── legal_name_match.py
│   │   │   ├── address_match.py
│   │   │   ├── turnover_threshold.py
│   │   │   ├── required_document_check.py
│   │   │   └── rule_registry.py
│   │   ├── entity_resolver.py
│   │   ├── contradiction_detector.py
│   │   ├── confidence_scorer.py
│   │   ├── evidence_linker.py
│   │   └── engine.py
│   │
│   ├── report_generator/
│   │   ├── report_data_builder.py
│   │   ├── pdf_report_builder.py
│   │   └── report_storage_service.py
│   │
│   ├── queue/
│   │   ├── consumers/
│   │   ├── producers/
│   │   ├── event_schemas/
│   │   └── tasks.py
│   │
│   ├── database/
│   │   ├── repositories/
│   │   └── models/
│   │
│   ├── shared/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   │
│   └── models/
│       ├── paddleocr/
│       └── layoutlmv3/
│
├── tests/
├── requirements.txt
└── pyproject.toml
```

---

## 17. Shared Packages Folder Structure

**Location:** **`packages/`**

```
packages/
├── shared-types/
│   ├── schemas/
│   │   ├── tender.schema.json
│   │   ├── bidder.schema.json
│   │   ├── document.schema.json
│   │   ├── extracted-field.schema.json
│   │   ├── compliance-flag.schema.json
│   │   ├── bounding-box.schema.json
│   │   └── graph-node.schema.json
│   ├── typescript/
│   ├── python/
│   └── README.md
│
├── api-contracts/
│   ├── openapi/
│   │   └── openapi.yaml
│   ├── graphql/
│   │   └── schema.graphql
│   ├── events/
│   │   ├── document.uploaded.json
│   │   ├── document.extraction.completed.json
│   │   ├── compliance.evaluation.completed.json
│   │   └── report.generated.json
│   └── README.md
│
├── ui-kit/
│   ├── components/
│   ├── tokens/
│   │   ├── colors.ts
│   │   ├── nodeColors.ts
│   │   └── typography.ts
│   └── styles/
│
└── config/
    ├── eslint/
    ├── typescript/
    ├── tailwind/
    └── testing/
```

---

## 18. Infrastructure and Documentation Structure

```
infra/
├── docker/
│   ├── docker-compose.yml
│   ├── web.Dockerfile
│   ├── api-gateway.Dockerfile
│   └── ai-workers.Dockerfile
│
├── kubernetes/
│   ├── web-deployment.yaml
│   ├── api-gateway-deployment.yaml
│   ├── ai-workers-deployment.yaml
│   ├── queue-deployment.yaml
│   └── configmaps/
│
├── terraform/
│   ├── object-storage/
│   ├── queue/
│   ├── database/
│   └── networking/
│
└── scripts/
    ├── seed-db.sh
    ├── migrate-db.sh
    ├── generate-contracts.sh
    └── run-local.sh

docs/
├── PRD.md
├── architecture/
│   ├── system-diagram.md
│   ├── data-flow.md
│   ├── event-catalog.md
│   └── api-guide.md
├── adr/
│   ├── 001-monorepo-architecture.md
│   ├── 002-event-driven-processing.md
│   └── 003-contract-first-development.md
└── runbooks/
    ├── upload-failure.md
    ├── worker-failure.md
    └── report-generation-failure.md
```

---

## 19. Feature-to-Folder Traceability Matrix

| **Feature** | **Frontend Module** | **API Gateway Module** | **AI Worker Module** |                                             |                                               |                                             |
| ------------------------------------------------------------ | ------------------------------------------- | --------------------------------------------- | ------------------------------------------- |
| Tender-Level Bidder Dashboard                                | **`apps/web/src/modules/bidder-dashboard`** | **`apps/api-gateway/src/modules/bidders`**    | —                                           |
| Batch Upload and Ingestion                                   | **`apps/web/src/modules/ingestion`**        | **`apps/api-gateway/src/modules/ingestion`**  | **`apps/ai-workers/src/ingestion_worker`**  |
| OCR and Layout Extraction                                    | **`apps/web/src/modules/evidence-viewer`**  | **`apps/api-gateway/src/modules/extraction`** | **`apps/ai-workers/src/ocr`**               |
| Contradiction and Uncertainty Engine                         | **`apps/web/src/modules/compliance-flags`** | **`apps/api-gateway/src/modules/compliance`** | **`apps/ai-workers/src/compliance_engine`** |
| Interactive Star Graph                                       | **`apps/web/src/modules/star-graph`**       | **`apps/api-gateway/src/modules/graph`**      | —                                           |
| In-Document Evidence Viewer                                  | **`apps/web/src/modules/evidence-viewer`**  | **`apps/api-gateway/src/modules/evidence`**   | —                                           |
| Explainable Officer Report                                   | **`apps/web/src/modules/officer-report`**   | **`apps/api-gateway/src/modules/reports`**    | **`apps/ai-workers/src/report_generator`**  |

---

## 20. Integration and Persistence Rules

To ensure a seamless product experience, GovFlow must follow the rules below.

### 20.1 Shared Contracts

- All API payloads must use schemas in **`packages/shared-types`** and **`packages/api-contracts`**.
- Frontend and workers must not define conflicting versions of shared entities.
- Contract changes must be versioned and validated in CI.

### 20.2 Persistent User Context

The frontend must persist:

```
Active Tender ID
Active Bidder ID
Active Document ID
Active Document Page
Selected Compliance Flag ID
Selected Evidence Anchor ID
Dashboard Filter State
Graph View State
```

Persistent context must be maintained through:

- URL route parameters
- Query parameters where appropriate
- Shared state stores
- Server-side loading from the API
- Browser refresh recovery

### 20.3 Module Boundaries

- Feature modules may use shared packages.
- Feature modules must not directly access private internals of another feature module.
- Cross-feature communication must happen through shared types, API calls, shared stores, or defined events.
- Business rules must remain in the Compliance Engine, not duplicated in frontend components.

### 20.4 Decision Integrity

- Officer decisions must never overwrite the original AI recommendation.
- Every decision must reference the evaluated flag.
- Every decision must create an audit event.
- Reports must show both AI and officer outcomes.

---

## 21. Security and Compliance Requirements

### 21.1 Access Control

GovFlow must support role-based access control.

Minimum roles:

```
Procurement Officer
Compliance Auditor
Tender Committee Member
System Administrator
```

### 21.2 Document Security

- Uploaded documents must be stored in secure object storage.
- Document access must use temporary signed URLs.
- Documents must not be publicly accessible.
- Sensitive bidder data must be encrypted at rest and in transit.
- Access to documents and reports must be logged.

### 21.3 Auditability

- Officer decisions must be immutable after recording.
- Audit logs must contain timestamps and user identity.
- Generated reports must preserve source evidence references.
- Deleted or replaced documents must retain historical audit context where legally required.

### 21.4 Data Retention

Data retention periods must be configurable based on procurement policy, legal requirements, and organizational governance rules.

---

## 22. Non-Functional Requirements

| **Category** | **Requirement** |                                                                                                      |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| Performance             | Dashboard and graph views should load quickly from pre-aggregated data                               |
| Processing              | OCR and compliance processing must run asynchronously                                                |
| Reliability             | Failed processing jobs must be retryable                                                             |
| Scalability             | Workers must support horizontal scaling for large bid package volumes                                |
| Availability            | Officers must be able to review completed data even while other documents are processing             |
| Observability           | APIs, workers, queue events, and failures must be logged and monitored                               |
| Accessibility           | Core dashboard, graph controls, and document navigation must support accessible interaction patterns |
| Testability             | Every module must include unit tests; integration workflows must include end-to-end tests            |
| Maintainability         | Shared contracts and modular boundaries must be enforced through code review and CI                  |

---

## 23. Testing Requirements

### 23.1 Unit Tests

Required for:

- Tender rule evaluation
- GSTIN matching
- Turnover validation
- Address and legal-name comparison
- Confidence scoring
- Coordinate scaling
- Node color mapping
- Report data assembly
- Officer decision recording

### 23.2 Integration Tests

Required workflows:

1. Upload document → create processing job.
2. Process document → extract fields and coordinates.
3. Extract fields → generate compliance flags.
4. Generate flags → update dashboard and graph.
5. Select graph node → open matching document viewer.
6. Select evidence box → open linked flag details.
7. Record officer decision → create audit event.
8. Generate report → include AI and officer decisions.

### 23.3 End-to-End Tests

Required officer flow:

```
Create/select Tender
   → Upload Bidder Package
   → Wait for Processing
   → Open Dashboard
   → Select Bidder
   → Open Star Graph
   → Open Evidence Viewer
   → Confirm/Reject/Override Finding
   → Generate Compliance Report
```

---

## 24. Execution Plan

| **Phase** | **Duration** | **Focus** | **Deliverables** |            |                            |                                                                                   |
| ---------------------------------- | ---------- | --- | --- | --------------------------------------------------------------------------------- |
| Phase 1                            | Days 1–3   | Core API and ingestion     | Upload API, storage, queue, document records, OCR integration, coordinate mapping |
| Phase 2                            | Days 4–6   | Compliance engine          | Entity extraction, tender rules, contradiction detection, missing document checks |
| Phase 3                            | Days 7–10  | UI innovation              | Dashboard, React Flow graph, evidence viewer, bounding-box overlays               |
| Phase 4                            | Days 11–14 | Integration and final flow | Live API integration, officer decisions, report generation, end-to-end testing    |

### 24.1 Phase-to-Folder Mapping

| **Phase** | **Primary Folders** |                                                                                                                                                       |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1                  | **`apps/api-gateway/src/modules/ingestion`**, **`apps/ai-workers/src/ingestion_worker`**, **`apps/ai-workers/src/ocr`**, **`packages/shared-types`**  |
| Phase 2                  | **`apps/ai-workers/src/compliance_engine`**, **`apps/api-gateway/src/modules/compliance`**, **`packages/api-contracts`**                              |
| Phase 3                  | **`apps/web/src/modules/bidder-dashboard`**, **`apps/web/src/modules/star-graph`**, **`apps/web/src/modules/evidence-viewer`**, **`packages/ui-kit`** |
| Phase 4                  | **`apps/web/src/modules/officer-report`**, **`apps/api-gateway/src/modules/reports`**, **`apps/web/src/shared`**, end-to-end test suites              |

---

## 25. Non-Goals for MVP

The following are outside the MVP scope:

- Direct live verification through government GST or Udyam APIs.
- Multi-lingual OCR support.
- Historical bidder risk scoring across multiple tenders.
- Automated bidder communication emails.
- Fully autonomous bidder rejection.
- Secondary approval workflows for officer overrides.
- Advanced predictive risk scoring based on historical procurement outcomes.

---

## 26. Future Scope

### 26.1 Government API Verification

Integration with government gateways for direct GST, Udyam, and business registration verification.

### 26.2 Multi-Lingual Document Processing

Support for regional languages and multilingual document extraction.

### 26.3 Vendor Risk History

Historical compliance profiles across tenders for identifying recurring non-compliance patterns.

### 26.4 Automated Clarification Workflows

Generation of officer-reviewed clarification requests for:

- Missing documents
- Low-confidence documents
- Invalid documents
- Contradictory bidder information

### 26.5 Secondary Approval Workflow

Approval chain for officer overrides, escalations, or high-value tender decisions.

---

## 27. Open Questions

1. What is the final list of tender rule types required for MVP launch?
2. What document types are mandatory for each tender category?
3. What are the legal data-retention requirements for bidder documents?
4. Does an officer override require a second-level approval process?
5. What scoring formula should be used for bidder compliance scores?
6. What file-size and document-count limits apply per bidder package?
7. Which object storage, queue, and database providers will be used in deployment?
8. What audit-log retention and export requirements apply to procurement reviews?

---

## 28. Glossary

| **Term** | **Definition** |                                                                                         |
| ------------------ | --------------------------------------------------------------------------------------- |
| Bidder             | A company or entity submitting a bid package for a tender                               |
| Tender             | A procurement opportunity with defined compliance requirements                          |
| OCR                | Optical Character Recognition                                                           |
| LayoutLMv3         | A layout-aware transformer model used for document understanding                        |
| Bounding Box       | Coordinate set defining a region on a document page                                     |
| Evidence Anchor    | A link between a finding and its exact source location in a document                    |
| Star Graph         | A graph visualization with bidder at the center and documents as connected nodes        |
| Compliance Flag    | A result created by the compliance engine based on document analysis and tender rules   |
| Contradiction      | A mismatch between values extracted from multiple source documents                      |
| Officer Decision   | A confirmation, rejection, override, or escalation made by a procurement officer        |
| Object Storage     | Secure storage used for original documents, pages, and generated reports                |
| Queue / Event Bus  | Infrastructure used to process ingestion, OCR, compliance, and reporting asynchronously |
| Monorepo           | A single repository containing multiple applications and shared packages                |
| Shared Contract    | A versioned schema shared by frontend, API, workers, and reporting modules              |

---

**End of Document**
