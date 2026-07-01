---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [java, testing, coverage, jacoco]
---

# Code Coverage and JaCoCo

Code coverage tools (like JaCoCo in Java) measure how many lines of production code are executed when the test suite runs.

## The Threshold Fallacy
Many projects enforce a minimum coverage threshold (e.g., 80% line coverage) failing the build if it drops below.
However, **coverage percentage alone is misleading**. A test can execute a method without making any meaningful assertions, thus "covering" the lines without actually testing the logic.

## Best Practices
- Focus on testing business logic, edge cases, and error paths.
- Do not write meaningless tests just to bump a percentage metric.
- Treat coverage as a floor (a tool to find completely untested areas) rather than a target to maximize blindly.
