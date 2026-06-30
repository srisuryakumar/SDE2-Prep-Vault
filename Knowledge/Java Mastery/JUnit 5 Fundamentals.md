---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, testing, junit]
---

# JUnit 5 Fundamentals

JUnit 5 is the standard testing framework for Java applications.

## Lifecycle Annotations
- `@BeforeAll` / `@AfterAll`: Runs once before/after all tests in the class. Must be static.
- `@BeforeEach` / `@AfterEach`: Runs before/after every single `@Test` method. Used to guarantee fresh state for each test.
- `@Test`: Marks a method as a test case.
- `@Disabled`: Temporarily disables a test (usually requires a reason like a Jira ticket).

## Advanced Features
- **Parameterized Tests:** `@ParameterizedTest` allows you to run the exact same test logic multiple times with different inputs using `@ValueSource` or `@CsvSource`.
- **Nested Tests:** `@Nested` allows you to group related tests in inner classes, sharing specific setup logic in their own `@BeforeEach` methods.
