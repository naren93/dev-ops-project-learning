# Angular App Customization: From Boilerplate to Documentation Portal

This document records the specific tweaks made to the "001-Hello-world" project to transform it into a "No-Nonsense" documentation guide for future viewers and GitHub portfolio visitors.

## 1. Objective
Replace the standard Angular "Welcome" page with the project's own architectural documentation (`angular-docker-setup.md`) to provide immediate value to anyone running the application.

## 2. Implementation Details

### HTML Structure (`src/app/app.html`)
- **Semantic Tags:** Used `<header>`, `<section>`, `<code>`, and `<footer>` to ensure the guide is structured and accessible.
- **Content Mapping:** Manually mapped the Markdown content from the PKB folder into clean HTML to avoid adding heavy Markdown-parsing libraries to the bundle, keeping the "Ultra-Clean" promise.

### Styling (`src/app/app.css`)
- **Typography:** Implemented a system-font stack (Apple/Segoe UI) for a "native" professional feel.
- **Readability:** Set a `max-width` of 800px and optimized `line-height` for technical reading.
- **Code Blocks:** Styled `<pre>` and `<code>` tags with a subtle background and borders to mimic GitHub/Technical-Blog aesthetics.

## 3. Key Benefits
- **Zero Bloat:** No external CSS frameworks (like Bootstrap/Tailwind) or Markdown libraries were used.
- **Self-Documenting:** The application is now its own manual.
- **Professional Polish:** Demonstrates a transition from "getting it to work" (infrastructure) to "delivering value" (UI/UX).

---
*Last updated: April 2026*
