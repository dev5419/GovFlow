# @govflow/api-contracts

This package contains the authoritative REST API specification, GraphQL schema stub, and asynchronous event contracts for the GovFlow monorepo.

---

## Structure

```
packages/api-contracts/
├── openapi/
│   └── openapi.yaml           # OpenAPI 3.1.0 specification covering §12.1 capabilities
├── graphql/
│   └── schema.graphql         # GraphQL SDL schema mirroring entities and queries
├── events/                    # Asynchronous event contracts (§11.3)
│   ├── document.uploaded.json
│   ├── document.preprocessed.json
│   ├── document.extraction.completed.json
│   ├── compliance.evaluation.completed.json
│   ├── report.requested.json
│   └── report.generated.json
├── package.json
└── README.md
```

---

## 1. REST API Capabilities (PRD §12.1)

All endpoints reference versioned entity schemas in `@govflow/shared-types` via `$ref`:

| Capability Area | Base Route | Key Operations |
|---|---|---|
| **Tenders** | `/tenders` | Create, retrieve, update tender workspaces, configure compliance rules, and set required documents |
| **Bidders** | `/tenders/{id}/bidders` | List participating bidders, retrieve compliance scores, and dashboard aggregations (F-01) |
| **Ingestion** | `/tenders/{id}/ingestion` | Batch bid-package upload (ZIP/PDF/images) and polling job progress (F-02) |
| **Documents** | `/documents` | Retrieve document metadata, page coordinate structures, and secure signed viewing URLs (PRD §21.2) |
| **Extraction** | `/documents/{id}/extractions` | Retrieve OCR and LayoutLMv3 extracted fields with confidence scores and bounding boxes (F-03) |
| **Compliance** | `/compliance/flags` | Retrieve anomaly flags, contradictions, record officer decisions (Pending/Confirmed/Rejected/Overridden/Escalated) (F-04) |
| **Graph** | `/tenders/{id}/bidders/{id}/graph` | Retrieve nodes, edges, and status color mappings for the interactive star graph (F-05) |
| **Evidence** | `/documents/{id}/pages/{page}/evidence-anchors` | Retrieve coordinate bounding-box overlays and linked conflicting document evidence (F-06) |
| **Reports** | `/tenders/{id}/bidders/{id}/reports` | Request, view, and download explainable compliance reports and decision logs (F-07) |
| **Audit** | `/tenders/{id}/audit-events` | Retrieve append-only officer decision history and audit trail (PRD §9.2) |

---

## 2. Event Catalog (PRD §11.3)

Every asynchronous message passed across Redis / Celery or the internal message bus must conform to the corresponding schema in `events/`:

| Event Schema | Producer | Consumer | Purpose |
|---|---|---|---|
| [`document.uploaded.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/document.uploaded.json) | API Gateway | Ingestion Worker | Start ingestion workflow, file validation, and storage |
| [`document.preprocessed.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/document.preprocessed.json) | Ingestion Worker | OCR Worker | Start page-level OCR and LayoutLMv3 extraction |
| [`document.extraction.completed.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/document.extraction.completed.json) | OCR Worker | Compliance Engine | Start rule evaluation and cross-document contradiction check |
| [`compliance.evaluation.completed.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/compliance.evaluation.completed.json) | Compliance Engine | API Gateway / Dashboard | Refresh bidder compliance summary and star graph |
| [`report.requested.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/report.requested.json) | API Gateway | Report Generator | Trigger PDF/HTML compliance report generation |
| [`report.generated.json`](file:///e:/Projects/GovFlow/packages/api-contracts/events/report.generated.json) | Report Generator | API Gateway | Deliver completed report access URL to officers |

---

## 3. Versioning Policy & CI Contract Validation (PRD §20.1)

GovFlow operates strictly on a **Contract-First** paradigm (PRD §6.5 & §20.1):

1. **No Undocumented Payloads**: No service, worker, router, or frontend component may introduce or consume ad-hoc or undocumented payloads. All request bodies, responses, and events must be formally defined here.
2. **Schema Reuse**: Public API payloads must directly reuse schemas from `packages/shared-types`. No duplicate or conflicting type definitions are permitted.
3. **CI Breaking-Change Detection**:
   - All contract modifications must be validated in CI before merge.
   - Breaking changes (field removal, enum alteration, stricter type constraints) require explicit major contract version bumps and coordinated client updates.
   - Event contracts must maintain backward compatibility for queued jobs.