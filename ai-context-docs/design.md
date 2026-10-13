# GCC Compass design system

This document records the existing prototype's visual conventions. It is not a request to redesign the app. Use these values as the baseline when extending its UI.

## Design direction

Calm, evidence-led research tooling for business decisions. Favor clear hierarchy, restrained color, legible data, and explicit trust/uncertainty cues over decorative dashboards or unsupported precision.

## Colors

| Token | Current value | Usage |
|---|---|---|
| Primary | `#3155A6` | Streamlit theme accent and primary controls |
| Background | `#FFFFFF` | Main page |
| Secondary background | `#F4F7FB` | Streamlit secondary surfaces |
| Text | `#15213A` | Theme text |
| Hero gradient | `#101C3A` to `#213C65` | Existing overview hero |
| Hero supporting text | `#D9E4F6` | Existing hero body text |
| Metric surface | `#F7F9FC` | Existing metric cards |
| Border / muted text | `#E5EAF2` / `#68758B` | Existing metric border and subdued labels |

The first four theme values are configured in `.streamlit/config.toml`. The hero, metric, and muted-label values are used by current inline CSS in `app.py`.

## Typography and layout

- **Font:** Streamlit sans-serif theme; no custom typeface is configured.
- **Hierarchy:** Streamlit page titles and headings, short captions for explanatory metadata, native widgets for controls.
- **Page width:** Wide layout; existing app CSS caps the content area at 1400px.
- **Spacing:** The current page uses approximately 1.4rem top padding and 2rem bottom padding, with compact metric-card padding.
- **Responsive behavior:** The app uses Streamlit columns for summary cards and provider records. Preserve usability when these wrap or stack at narrower widths.

No formal type-size scale or spacing-token system is implemented. Do not invent one as if it already exists.

## Components and patterns

- **Navigation:** Sidebar radio selector with six named research views.
- **Overview:** Dark gradient hero, four summary metrics, three decision prompts, and a recent-signals table.
- **Metrics:** Light surface, thin border, rounded corners.
- **Provider entries:** Bordered Streamlit containers with information and source-action columns.
- **Data tables:** Native `st.dataframe` with hidden index; source fields use link-column configuration where available.
- **Trust cues:** Use plain-language captions, info, and warning callouts to distinguish guidance and evidence limitations.
- **Links:** Label source actions clearly and make them open the underlying evidence.

## Interaction and accessibility

- Keep widget labels descriptive and associated with their inputs.
- Keep evidence status and prototype limitations available as text.
- Do not convey evidence strength through color alone.
- Preserve keyboard-operable native Streamlit controls.
- Keep data tables readable and retain meaningful column names.

## Styling guidance

- Use the configured Streamlit theme and native components for new UI.
- Existing CSS is part of the current prototype. Avoid expanding its dependence on Streamlit's internal DOM selectors; change existing CSS only when needed for an explicitly scoped UI task.
- Avoid an unrelated redesign, new color palette, or decorative chart without product justification.
