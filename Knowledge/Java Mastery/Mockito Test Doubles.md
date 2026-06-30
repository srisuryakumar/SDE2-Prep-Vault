---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, testing, mockito, mocks, spies]
---

# Mockito Test Doubles

Mockito is the standard Java library for creating test doubles (mocks and spies) to isolate the unit under test.

## @Mock vs @Spy
- **`@Mock`:** Creates a completely fake object. None of its real methods execute. All method calls return default values (`null`, `0`, `false`) unless explicitly stubbed using `when(mock.method()).thenReturn(value)`. Used to fully isolate a class from its dependencies.
- **`@Spy`:** Wraps a *real* object instance. Calling a method on a spy executes the REAL implementation by default. You can selectively override specific method behaviors using `doReturn(value).when(spy).method()`. Used when you need mostly-real behavior but want to override one specific interaction (e.g., an expensive external call).

## Key Mockito Concepts
- **Stubbing:** Defining what a mock should do when a method is called (`when(...).thenReturn(...)` or `thenThrow(...)`).
- **Verification:** Checking that the unit under test actually called a dependency correctly (`verify(mock).method()`).
- **Argument Captors:** Capturing the arguments passed to a mock method so you can assert on their values.
