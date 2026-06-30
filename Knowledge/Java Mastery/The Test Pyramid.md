---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, testing, pyramid]
---

# The Test Pyramid

The Test Pyramid is a foundational concept in software testing, describing the ideal distribution of different types of tests in a codebase.

## The Layers
1. **Unit Tests (The Base):** 
   - **Quantity:** Many (thousands)
   - **Speed:** Fast (milliseconds)
   - **Scope:** Isolated to a single class/method. Dependencies are mocked.
   - **Execution:** Run constantly (on every save/commit).
2. **Integration Tests (The Middle):**
   - **Quantity:** Some (hundreds)
   - **Speed:** Moderate (seconds)
   - **Scope:** Tests interaction between components (e.g., Database, Message Queue, External API). Real or containerized dependencies are used.
   - **Execution:** Run before commit or PR merge.
3. **End-to-End (E2E) Tests (The Peak):**
   - **Quantity:** Few (dozens)
   - **Speed:** Slow (minutes)
   - **Scope:** Tests the entire system from the user's perspective (UI to Database).
   - **Execution:** Run in CI before deployment.

Each layer up trades speed and isolation for realism. A healthy test suite is heavy on the bottom and light on the top.
