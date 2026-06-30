---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 9 — Modern Java Features"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, switch, expressions]
---

# Java Switch Expressions

Introduced in Java 14, switch expressions modernize the `switch` statement.

## Key Improvements
- **Arrow Syntax (`->`):** Eliminates fall-through behavior (no `break` needed).
- **Multiple Cases:** `case MONDAY, FRIDAY, SUNDAY -> ...`
- **Expressions:** The switch can return a value directly.
- **Exhaustiveness:** If switching on an enum (or sealed class), the compiler ensures all cases are covered. If you add a new enum value later, the compile fails instead of failing silently at runtime.

```java
int numLetters = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY                -> 7;
    case THURSDAY, SATURDAY     -> 8;
    case WEDNESDAY              -> 9;
    // No default needed if all enums are covered
};
```

## Yielding from Blocks
If a case requires multiple statements before returning a value, use a block `{}` and the `yield` keyword instead of `return`.
```java
int result = switch (day) {
    case MONDAY -> 1;
    default -> {
        System.out.println("Calculating default...");
        yield 0;
    }
};
```
