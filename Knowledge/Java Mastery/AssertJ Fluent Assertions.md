---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 8 — Testing Java Applications"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, testing, assertj, assertions]
---

# AssertJ Fluent Assertions

`AssertJ` is a library that provides a much more readable, fluent assertion API than the raw JUnit assertions (`assertEquals`).

## Why Use AssertJ?
- **Readability:** `assertThat(name).isEqualTo("Surya")` reads like English.
- **Chainability:** `assertThat(name).startsWith("S").endsWith("a").hasSize(5)`
- **Rich Collection Support:** `assertThat(list).containsExactlyInAnyOrder("A", "B")`

## Soft Assertions
Normally, a test stops executing at the first failed assertion. `SoftAssertions` collect ALL failures in a test and report them all at once at the end.
```java
SoftAssertions softly = new SoftAssertions();
softly.assertThat(name).isEqualTo("RightName"); // fails, but doesn't stop
softly.assertThat(score).isEqualTo(100);        // fails, but doesn't stop
softly.assertAll(); // Reports BOTH failures together
```
