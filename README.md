# GovFlow

Interactive audit and compliance platform for procurement officers evaluating tender bid packages.

## Monorepo Structure

| Directory | Purpose |
|---|---|
| `apps/web/` | Next.js 14 frontend — dashboards, star graph, evidence viewer |
| `apps/api-gateway/` | FastAPI backend — REST API, auth, event publishing |
| `apps/ai-workers/` | Python workers — ingestion, OCR, compliance engine, reports |
| `packages/shared-types/` | Versioned JSON schemas shared across all apps |
| `packages/api-contracts/` | OpenAPI specs, GraphQL schema, event contracts |
| `packages/ui-kit/` | Shared UI components and design tokens |
| `packages/config/` | Shared ESLint, TypeScript, Tailwind, and test configs |
| `infra/` | Docker, Kubernetes, Terraform, deployment scripts |
| `docs/` | Architecture docs, ADRs, runbooks |

## Getting Started

```bash
pnpm install
pnpm dev
```

See individual app READMEs for app-specific setup.
