---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, ide]
---

# IntelliJ IDEA Productivity and Debugging

IntelliJ IDEA is the premier Java IDE. Mastering it makes development significantly faster.

## Navigation Shortcuts
- **Find anything:** Shift Shift
- **Go to class:** Cmd+O (Mac) / Ctrl+N (Win)
- **Go to file:** Cmd+Shift+O (Mac) / Ctrl+Shift+N (Win)
- **Go to declaration:** Cmd+B (Mac) / Ctrl+B (Win)
- **Recent files:** Cmd+E (Mac) / Ctrl+E (Win)

## Debugging
Setting breakpoints and stepping through code is far superior to `System.out.println`.
- **Conditional Breakpoints:** Right-click a breakpoint to add a condition (e.g., `orderId.equals("123")`). The debugger only pauses if the condition is true.
- **Stepping:**
  - Step Over (F8): Move to the next line.
  - Step Into (F7): Enter a method call.
  - Step Out (Shift+F8): Return from the current method.
- **Evaluate Expression (Alt+F8):** Allows you to execute arbitrary Java code in the context of the paused application to test hypotheses on the fly.
