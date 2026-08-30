---
name: govflow-prd
description: >
  Product requirements reference for GovFlow. Read this skill when you need
  to understand feature scope, data models, API contracts, module boundaries,
  user journeys, or acceptance criteria. Always consult the full PRD for
  authoritative details.
---

# GovFlow PRD Reference Skill

## When to Activate

Activate this skill when:

- Planning or implementing any MVP feature (F-01 through F-07)
- Defining or modifying data models, API contracts, or event schemas
- Making decisions about module boundaries or cross-module communication
- Writing acceptance tests or verification criteria
- Resolving ambiguity about what a feature should or should not do
- Working on officer decisions, audit trails, or compliance logic

## Required Steps

1. **Read the full PRD**: Open [`GovFlow_PRD.md`](file:///e:/Projects/GovFlow/GovFlow_PRD.md) and read the sections relevant to your task.
2. **Respect module boundaries**: Features are independent modules (PRD §6.4). Don't leak internals across modules — use shared types, API calls, or events (PRD §20.3).
3. **Use shared contracts**: All API payloads must use schemas from `packages/shared-types` and `packages/api-contracts` (PRD §20.1).
4. **Preserve decision integrity**: Officer decisions never overwrite AI recommendations. Every decision creates an audit event (PRD §20.4).

## MVP Features Quick Map

| ID | Feature | Frontend Module | Backend Module | AI Worker |
|---|---|---|---|---|
| F-01 | Tender Dashboard | `bidder-dashboard` | `bidders` | — |
| F-02 | Batch Upload | `ingestion` | `ingestion` | `ingestion_worker` |
| F-03 | OCR + Field Extraction | `evidence-viewer` | `extraction` | `ocr` |
| F-04 | Compliance Engine | `compliance-flags` | `compliance` | `compliance_engine` |
| F-05 | Star Graph | `star-graph` | `graph` | — |
| F-06 | Evidence Viewer | `evidence-viewer` | `evidence` | — |
| F-07 | Officer Report | `officer-report` | `reports` | `report_generator` |

## Core Data Entities

`Tender` · `TenderRule` · `RequiredDocument` · `Bidder` · `Document` · `DocumentPage` · `ProcessingJob` · `ExtractedField` · `EvidenceAnchor` · `ComplianceFlag` · `OfficerDecision` · `AuditEvent` · `BidderComplianceSummary`

## Required Events

| Event | Producer → Consumer |
|---|---|
| `document.uploaded` | API Gateway → Ingestion Worker |
| `document.preprocessed` | Ingestion Worker → OCR Worker |
| `document.extraction.completed` | OCR Worker → Compliance Engine |
| `compliance.evaluation.completed` | Compliance Engine → API Gateway |
| `report.requested` | API Gateway → Report Generator |
| `report.generated` | Report Generator → API Gateway |

## Compliance Flag Statuses

`Verified` · `Potential Non-Compliance` · `Needs Review` · `Insufficient Evidence` · `Missing`

## Officer Decision States

`Pending` · `Confirmed` · `Rejected` · `Overridden` · `Escalated`

## Key Principles

1. **Evidence-First**: Every finding must have document source + page + bounding box.
2. **Human-in-the-Loop**: GovFlow recommends, officers decide. No auto-rejection.
3. **Persistent Context**: Tender → Bidder → Document → Flag → Page must survive navigation and refresh.
4. **Contract-First**: Shared versioned schemas, no undocumented payloads.
5. **Append-Only Audit**: Audit records are immutable. Prior decisions remain visible.

## Execution Phases

| Phase | Days | Focus |
|---|---|---|
| 1 | 1–3 | Core API, ingestion, OCR integration |
| 2 | 4–6 | Compliance engine, rules, contradiction detection |
| 3 | 7–10 | Dashboard, React Flow graph, evidence viewer, overlays |
| 4 | 11–14 | Integration, officer decisions, reports, E2E testing |

## Non-Goals (MVP)

- No live government API verification (GST/Udyam)
- No multi-lingual OCR
- No historical bidder risk scoring
- No automated bidder communication
- No auto-rejection
- No secondary approval workflows
