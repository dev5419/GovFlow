# DESIGN.md

## Visual Theme & Atmosphere

The Government e-Marketplace (GeM) visual theme embodies an institutional, high-trust sovereign e-commerce and public procurement platform compliant with Guidelines for Indian Government Websites (GIGW) and WCAG 2.1 AA. The aesthetic is utilitarian, dense, and structured, prioritizing transactional efficiency, legibility, and high visual contrast over decorative flourishes. Deep navy blue conveys authority and stability, paired with vibrant saffron/amber accents for critical actions and national identity. Surfaces are clean, crisp, and high-contrast, structured with subtle borders, restrained elevations, and modular data grids tailored for institutional buyers and enterprise sellers.

## Color Palette & Roles (CSS variables)

CSS

```
:root {
  --color-primary: #0C2340;          /* Deep Navy - Header & Brand Primary */
  --color-primary-variant: #1B365D;  /* Slate Navy - Utility Nav & Accents */
  --color-accent: #F37021;           /* Saffron/Orange - Primary CTA */
  --color-accent-hover: #D95C0F;     /* Darker Orange - Hover State */
  --color-secondary: #138808;        /* India Green - Success & Badges */
  --color-bg-base: #F8F9FA;          /* Neutral Light - Page Canvas */
  --color-surface: #FFFFFF;          /* Pure White - Cards & Containers */
  --color-surface-alt: #F1F4F8;      /* Off-White - Inset Containers */
  --color-text-primary: #212529;     /* Charcoal - High-Contrast Body */
  --color-text-secondary: #595959;   /* Muted Gray - Secondary Captions */
  --color-border: #DDE2E5;           /* Light Gray - Card & Grid Dividers */
  --color-focus: #0C2340;            /* Deep Blue - Accessible Focus Ring */
}
```

## Typography Rules (scale + stack)

- **Font Stack**: `"Open Sans", "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif`
- **Indic/Devanagari Fallback**: `"Noto Sans Devanagari", "Mangal", sans-serif`
- **Licensing**: Open Source (SIL Open Font License / Apache 2.0 / System Fonts).
- **Scale**:
  - **Display / Hero**: `32px` (`2rem`) | Weight: `700` | Line-height: `1.25`
  - **H1**: `28px` (`1.75rem`) | Weight: `700` | Line-height: `1.3`
  - **H2**: `22px` (`1.375rem`) | Weight: `600` | Line-height: `1.35`
  - **H3**: `18px` (`1.125rem`) | Weight: `600` | Line-height: `1.4`
  - **Body**: `14px` (`0.875rem`) | Weight: `400` | Line-height: `1.5`
  - **Small / Caption**: `12px` (`0.75rem`) | Weight: `400` / `500` | Line-height: `1.4`

## Component Stylings (button, card, input, nav)

- **Primary Button**: Solid `--color-accent` (`#F37021`), text `#FFFFFF`, padding `8px 20px`, border-radius `4px`, border `1px solid transparent`, font-weight `600`, font-size `14px`. Hover: `--color-accent-hover` (`#D95C0F`).
- **Secondary Button**: Background `transparent`, border `1px solid #0C2340`, text `#0C2340`, border-radius `4px`, padding `8px 18px`, font-weight `600`.
- **Card**: Background `#FFFFFF`, border `1px solid #DDE2E5`, border-radius `4px`, padding `16px 20px`, box-shadow `0 1px 3px rgba(0,0,0,0.08)`.
- **Input & Search**: Background `#FFFFFF`, border `1px solid #C4CDD5`, border-radius `4px`, height `40px`, padding `6px 12px`, font-size `14px`. Focus: `outline: 2px solid #0C2340`, offset `1px`.
- **Navigation**: Top utility bar in `#1B365D` (`32px` height, `12px` text). Main navigation bar in `#0C2340` with white text, `10px 16px` padding, and active indicator with `3px solid #F37021` bottom border.

## Layout Principles (grid, max-width, spacing scale)

- **Max Width**: `1200px` centered container (`margin: 0 auto`, `padding: 0 16px`).
- **Grid**: 12-column responsive grid with `24px` gutters on desktop, collapsing to `16px` on mobile.
- **Spacing Scale**:
  - `4px` (`space-1`): Micro gaps & tag padding
  - `8px` (`space-2`): Button vertical padding, icon gaps
  - `12px` (`space-3`): Input inner padding
  - `16px` (`space-4`): Card inner padding, base gutter
  - `24px` (`space-5`): Section margins, card grid gaps
  - `32px` (`space-6`): Hero inner padding, container separation
  - `48px` (`space-7`): Major section blocks

## Depth & Elevation

- **Level 0 (Flat)**: `box-shadow: none;` applied to page canvas, utility toolbars, and standard form controls.
- **Level 1 (Cards & Panels)**: `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);`
- **Level 2 (Dropdowns & Card Hover)**: `box-shadow: 0 4px 8px -1px rgba(0, 0, 0, 0.12), 0 2px 4px -1px rgba(0, 0, 0, 0.06);`
- **Level 3 (Modals & Sticky Headers)**: `box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.05);`

## Do's and Don'ts

- **Do**:
  - Maintain WCAG 2.1 AA color contrast ratios (minimum 4.5:1 for body text).
  - Reserve `--color-accent` (`#F37021`) strictly for primary CTAs and interactive actions.
  - Implement visible `2px` focus rings on all interactive elements.
  - Use modular `4px` border-radii for a structured, institutional feel.
- **Don't**:
  - Do not use rounded pill shapes (`border-radius > 8px`) or heavy glassmorphism.
  - Do not use muted text lighter than `#595959` on light backgrounds.
  - Do not introduce non-functional micro-animations or excessive motion.
  - Do not hide critical procurement navigation within unlabeled icons.

## Responsive Behavior

- **Desktop (`>= 1200px`)**: Full 12-column layout, multi-tier horizontal navigation, fixed search bar with integrated category selector.
- **Laptop / Tablet Landscape (`992px - 1199px`)**: 12-column layout with compressed menu margins, max-width `960px`.
- **Tablet Portrait (`768px - 991px`)**: 2-to-4 column modular cards, consolidated search bar, collapsible hamburger navigation.
- **Mobile (`< 768px`)**: Single-column stacked layout, full-width buttons (`width: 100%`), sticky utility bar, horizontal scroll for data tables.

## Agent Prompt Guide

When generating UI components for the GeM platform:

- Use semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).
- Apply deep navy (`#0C2340`) for headers/containers and vibrant saffron (`#F37021`) for primary submission buttons and active states.
- Set base body text to `14px` / `1.5` line-height using `"Open Sans", "Roboto", sans-serif`.
- Enforce `4px` border-radius and `1px solid #DDE2E5` border on all cards and input components.
- Ensure strict keyboard accessibility with `outline: 2px solid #0C2340` on focus states.
