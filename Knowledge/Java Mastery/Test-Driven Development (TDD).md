---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, testing, tdd]
---

# Test-Driven Development (TDD)

TDD is a software development process relying on a very short development cycle: requirements are turned into specific test cases, and then the software is improved so that the tests pass.

## The Cycle (Red → Green → Refactor)
1. **Red:** Write a failing test *first*, before writing any implementation code. This forces you to think about the API contract and expected behavior.
2. **Green:** Write the absolute *minimum* amount of code necessary to make the failing test pass. Don't add extra features yet.
3. **Refactor:** Clean up the implementation code while keeping the tests green. Because you have a passing test, you can refactor confidently without fear of breaking functionality.

## Benefits
- Forces you to design from the caller's perspective.
- Guarantees test coverage (you can't write untested code).
- Produces a regression suite as a natural side effect of development.
