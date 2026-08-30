# @govflow/shared-types

This package provides the authoritative, single source of truth for all shared data models, entities, enums, and contracts across the entire GovFlow monorepo.

## Architectural Purpose & Parity Guarantee

GovFlow is a hybrid TypeScript (Next.js frontend in `apps/web/`) and Python (FastAPI backend in `apps/api-gateway/`, Celery workers in `apps/ai-workers/`) monorepo.

To maintain strict architectural boundaries (PRD §6.5, §12.2, §20.1, §20.3):
1. **JSON Schemas (`schemas/`)**: Language-agnostic, versioned JSON Schema definitions (Draft 2020-12) defining the structural contract for every core entity.
2. **TypeScript Types (`typescript/`)**: Strict TypeScript interfaces and type unions for the Next.js frontend, state stores, and UI components.
3. **Python Pydantic Models (`python/`)**: Pydantic v2 `BaseModel` classes with camelCase alias support and field validation for FastAPI routers and AI workers.
4. **Parity Guarantee**: Every field, type constraint, optionality rule, and enum value is kept in exact 1:1 synchronization across JSON Schema, TypeScript, and Python definitions.

> [!IMPORTANT]
> **No Duplicate Types Rule**: Downstream applications and packages (`apps/web`, `apps/api-gateway`, `apps/ai-workers`, `packages/api-contracts`, `packages/ui-kit`) **MUST NEVER** define internal duplicate versions of these entities. All consumer modules must import types directly from `@govflow/shared-types` (TS) or `packages/shared-types/python` (Python).

---

## Core Entities Included

| Entity | PRD Section | Description |
|---|---|---|
| `BoundingBox` | §12.3 | Document coordinate contract (`pageNumber`, `pageWidth`, `pageHeight`, `x1`, `y1`, `x2`, `y2`) |
| `ComplianceFlag` | §12.4 | Rule evaluation result, anomaly finding, or contradiction record |
| `OfficerDecision` | §9.1, §10 | Procurement officer decision record (`Pending`, `Confirmed`, `Rejected`, `Overridden`, `Escalated`) |
| `AuditEvent` | §9.2, §10 | Immutable, append-only audit trail record capturing all officer actions and recommendations |
| `Tender` | §10 | Procurement opportunity workspace |
| `TenderRule` | §10 | Tender-specific compliance rule configuration |
| `RequiredDocument` | §10 | Mandatory or optional document requirement definition |
| `Bidder` | §10 | Bidder vendor entity submitting a bid package |
| `Document` | §10 | Uploaded bidder document record |
| `DocumentPage` | §10 | Individual page in a multipage document with dimension metadata |
| `ProcessingJob` | §10 | Async pipeline task state for ingestion, OCR, compliance, and reporting |
| `ExtractedField` | §8.3, §10 | OCR and LayoutLM-extracted field with confidence score and bounding box |
| `EvidenceAnchor` | §8.6, §10 | Coordinate anchor linking compliance findings to visual document canvas |
| `GraphNode` | §8.5, §10 | Interactive star topology graph node with semantic color mapping |
| `GraphEdge` | §8.5, §10 | Star graph edge connecting bidder to document node or contradiction link |
| `BidderComplianceSummary` | §8.1, §10 | Aggregated compliance score and risk summary for the tender dashboard |

---

## Import Examples

### In TypeScript / Next.js (`apps/web/`)

```typescript
import type {
  Tender,
  Bidder,
  ComplianceFlag,
  ComplianceFlagStatus,
  BoundingBox,
  OfficerDecision,
  GraphNode,
  BidderComplianceSummary,
} from "@govflow/shared-types";
```

### In Python / FastAPI / Celery (`apps/api-gateway/`, `apps/ai-workers/`)

```python
# Direct import from the shared-types package
from packages.shared_types.python import (
    Tender,
    Bidder,
    ComplianceFlag,
    ComplianceFlagStatus,
    BoundingBox,
    OfficerDecision,
    OfficerDecisionState,
    AuditEvent,
    ProcessingJob,
    ExtractedField,
    BidderComplianceSummary,
)
```

---

## Immutable Audit Trail Guarantee

Per PRD §9.2 and §20.4, `AuditEvent` is strictly **append-only**:
- In TypeScript, all fields are marked `readonly`.
- In Python, the model uses `model_config = ConfigDict(frozen=True)`.
- No modification or deletion interfaces are provided.