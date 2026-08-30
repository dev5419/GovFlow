---
name: govflow-techstack
description: >
  Mandatory tech stack reference for all GovFlow development. Read this skill
  before writing code, adding dependencies, or making architecture decisions
  to ensure alignment with the locked technology choices.
---

# GovFlow Tech Stack Skill

## When to Activate

Activate this skill **before**:

- Writing or scaffolding any new code (frontend, backend, or AI worker)
- Adding a new dependency or library
- Making architecture or infrastructure decisions
- Setting up build tooling, Docker config, or CI/CD

## Required Steps

1. **Read the tech stack doc**: Open and read [`techstack.md`](file:///e:/Projects/GovFlow/techstack.md) in full.
2. **Verify your choice**: Before introducing ANY library, framework, or tool, check if the tech stack already specifies one for that purpose. If it does, use it — do not substitute.
3. **Check the PRD structure**: If you need folder/module guidance, read the relevant sections of [`GovFlow_PRD.md`](file:///e:/Projects/GovFlow/GovFlow_PRD.md) (§13–§18 for folder structures, §19 for feature-to-folder mapping).

## Locked Stack Summary (Quick Reference)

Always verify against [`techstack.md`](file:///e:/Projects/GovFlow/techstack.md) for the authoritative list.

### Frontend
| Concern | Technology |
|---|---|
| Framework | **Next.js** (React 18) |
| Styling | **Tailwind CSS** + **Shadcn UI** |
| Graph visualization | **React Flow** |
| Document/PDF viewer | **react-pdf** + HTML5 Canvas / absolute-positioned DOM |
| State management | **Zustand** |

### Backend
| Concern | Technology |
|---|---|
| Framework | **FastAPI** (Python 3.10+) |
| Task queue | **Celery** + **Redis** |
| Authentication | JWT via **FastAPI-Users** |

### AI & Data Extraction
| Concern | Technology |
|---|---|
| OCR | **PaddleOCR** |
| Document understanding | **LayoutLMv3** (HuggingFace Transformers) |
| Image processing | **OpenCV** + **Pillow** |

### Database & Storage
| Concern | Technology |
|---|---|
| Primary DB | **PostgreSQL 15** |
| Flexible JSON storage | PostgreSQL **JSONB** columns |
| Object storage | **MinIO** (S3-compatible) |

### Infrastructure
| Concern | Technology |
|---|---|
| Containerization | **Docker** + **Docker Compose** |

## Rules

1. **Do not substitute locked technologies.** If `techstack.md` says React Flow for graphs, don't use D3, vis.js, or Cytoscape.
2. **Do not add new dependencies without justification.** If a locked technology or the standard library covers it, use that.
3. **Frontend is TypeScript + Next.js.** Don't scaffold with Vite, CRA, or plain React.
4. **Backend is Python + FastAPI.** Don't use Express, NestJS, Django, or Flask.
5. **AI workers are Python.** They share the FastAPI backend's Python ecosystem.
6. **Monorepo structure per PRD §13.** Apps go in `apps/`, shared code in `packages/`.

## Architecture Quick Reference

```
Officer → Next.js Web App → FastAPI API Gateway → PostgreSQL / MinIO
                                    ↓
                              Redis + Celery
                                    ↓
                    Ingestion Worker → OCR Worker → Compliance Engine
                                                        ↓
                                                  Report Generator
```

All services orchestrated via Docker Compose. Processing is async via Celery/Redis event queue.
