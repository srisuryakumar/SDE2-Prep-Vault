---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations, applications, desktop]
---

# Desktop Applications (Native vs Electron)

## Native Desktop Applications
Compiled to machine code for a specific OS (Swift for macOS, C++ for Windows). They use the OS's native UI frameworks.
- **Pros:** Fast, low memory footprint, direct OS API access.
- **Cons:** Requires a separate codebase for each OS.

## Electron Applications
Electron (used by VS Code, Slack, Postman) bundles a full Chromium browser engine and Node.js into a single package. The app is written in web technologies (HTML/CSS/JS) and runs inside this embedded browser.
- **Pros:** One codebase runs on macOS, Windows, and Linux. Fast development velocity.
- **Cons:** High resource usage. Every Electron app bundles its own ~100MB Chromium instance and runs multiple processes. A single app can consume 500MB+ of RAM just to display a UI.
