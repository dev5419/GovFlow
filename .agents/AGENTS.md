# GovFlow Development Rules

## Before Writing Any Code

1. **Read the tech stack first.** Before writing code, adding dependencies, or scaffolding anything, read the `govflow-techstack` skill. Use ONLY the locked technologies in `techstack.md`. Do not substitute.

2. **Read the PRD for context.** Before implementing any feature, read the `govflow-prd` skill to understand scope, acceptance criteria, data models, and module boundaries. Consult the full `GovFlow_PRD.md` for authoritative detail.

## Before Writing Any Frontend Code

3. **Read the design system.** Before creating or modifying any UI component, page, style, or layout, read the `govflow-design-system` skill. Apply every rule from `design.md` — colors, typography, spacing, elevation, components, responsive breakpoints, accessibility. No exceptions.

## General

4. **Monorepo structure.** Follow the folder structure in `GovFlow_PRD.md` §13–§18. Apps in `apps/`, shared code in `packages/`.

5. **Shared contracts.** All API payloads use schemas from `packages/shared-types` and `packages/api-contracts`. Frontend and workers must not define conflicting types.

6. **Module isolation.** Feature modules do not import from another feature module's internals. Cross-feature communication goes through shared types, API calls, shared stores, or events.
