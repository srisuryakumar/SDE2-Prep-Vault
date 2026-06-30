---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, boot, startup]
---

# ApplicationRunner and CommandLineRunner

## Intuition
If you want code to run exactly once at startup, after the application is fully wired, but before it starts accepting HTTP traffic, you use `ApplicationRunner` or `CommandLineRunner`.

## Why not static block or @PostConstruct?
- **`static` block:** Runs at class-loading time. The Spring context doesn't exist yet, so no beans are available.
- **`@PostConstruct`:** Runs per-bean as soon as that bean is wired. It guarantees the bean's own dependencies are ready, but NOT that the entire application context is fully constructed.
- **`ApplicationRunner#run()`:** Executes specifically after the whole context has finished refreshing (every singleton exists and is initialized), which is the only correctly-ordered hook for running logic exactly when the app is genuinely ready.
