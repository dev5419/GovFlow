---
name: govflow-design-system
description: >
  Mandatory design system reference for all frontend/UI work in GovFlow.
  Read this skill before creating, modifying, or reviewing any component,
  page, style, or layout in the apps/web/ or packages/ui-kit/ directories.
---

# GovFlow Design System Skill

## When to Activate

Activate this skill **before writing or modifying any frontend code**, including:

- React components (`.tsx`, `.jsx`)
- CSS / style files (`.css`, `.module.css`)
- Tailwind config or theme tokens
- Shadcn UI component overrides
- Layout or page templates
- UI-kit package components or tokens

## Required Steps

1. **Read the design spec**: Open and read [`design.md`](file:///e:/Projects/GovFlow/design.md) in full before writing any UI code.
2. **Apply the design tokens**: Use the CSS variables, typography scale, spacing scale, elevation levels, and component stylings defined in `design.md`. Do NOT invent ad-hoc colors, font sizes, or spacing values.
3. **Follow the Do's and Don'ts**: The design doc has explicit rules — no pill shapes, no glassmorphism, no muted text lighter than `#595959`, no non-functional micro-animations, no hidden icon-only navigation.
4. **Follow the Agent Prompt Guide**: The bottom section of `design.md` contains direct instructions for AI agents generating UI.

## Key Design Constraints (Quick Reference)

These are extracted from `design.md` — always verify against the source file for the latest values.

| Token | Value |
|---|---|
| Primary (headers/brand) | `#0C2340` Deep Navy |
| Accent (CTA buttons) | `#F37021` Saffron |
| Accent hover | `#D95C0F` |
| Success/badges | `#138808` India Green |
| Page background | `#F8F9FA` |
| Card surface | `#FFFFFF` |
| Body text | `#212529` Charcoal |
| Secondary text | `#595959` (minimum contrast) |
| Border | `#DDE2E5` |
| Focus ring | `2px solid #0C2340` |

- **Font stack**: `"Open Sans", "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`
- **Base body**: `14px / 1.5 line-height`
- **Border radius**: `4px` everywhere (max `8px`)
- **Max width**: `1200px` centered
- **Grid**: 12-column, `24px` gutters desktop, `16px` mobile

## Visual Style

This is a **government institutional platform** (GeM-inspired). The aesthetic is:
- Utilitarian, dense, and structured
- High-contrast, WCAG 2.1 AA compliant
- Crisp borders, restrained elevation, modular data grids
- Deep navy authority + saffron accent for actions
- NO decorative flourishes, NO glassmorphism, NO pill buttons

## Responsive Breakpoints

| Breakpoint | Layout |
|---|---|
| `≥ 1200px` | Full 12-column, multi-tier nav |
| `992px – 1199px` | 12-column compressed, `960px` max |
| `768px – 991px` | 2-4 column cards, hamburger nav |
| `< 768px` | Single column, full-width buttons, sticky utility bar |

## Checklist Before Committing Frontend Code

- [ ] All colors come from `design.md` CSS variables
- [ ] Typography uses the defined scale and font stack
- [ ] Spacing uses the `4px`-based scale (`space-1` through `space-7`)
- [ ] Cards have `1px solid #DDE2E5` border and `4px` border-radius
- [ ] Buttons follow Primary/Secondary button specs
- [ ] Focus states use `outline: 2px solid #0C2340`
- [ ] No `border-radius > 8px` used
- [ ] Semantic HTML5 elements used (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- [ ] WCAG 2.1 AA contrast ratios met (4.5:1 minimum for body text)
