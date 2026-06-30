---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, optional, null]
---

# Java Optional

`Optional<T>` is a container type introduced in Java 8 that may or may not contain a non-null value. It is meant to be a safe, explicit alternative to returning `null` from a method, forcing the caller to handle the "not found" or "absent" case.

## Creating Optionals
- `Optional.of(value)`: Returns an Optional containing the value. If the value is null, it throws a `NullPointerException` immediately.
- `Optional.ofNullable(value)`: If the value is null, returns `Optional.empty()`; otherwise returns an Optional containing the value.
- `Optional.empty()`: Returns an empty Optional.

## Best Practices
You should almost **never call `.get()` directly** without checking `isPresent()`, as this defeats the purpose of `Optional` (it throws `NoSuchElementException` if empty, which is no better than a `NullPointerException`).
Instead, use functional methods to handle the presence or absence safely:
- `.map()` and `.flatMap()` to transform the value if present.
- `.orElse(defaultValue)` to provide a fallback value.
- `.orElseGet(() -> expensiveDefaultComputation())` to lazily provide a fallback.
- `.orElseThrow(() -> new Exception(...))` to throw an exception if absent.
- `.ifPresent(Consumer)` to execute code only if the value exists.

## Anti-Patterns
- Using `Optional` as a method parameter. (Just pass the value or null directly).
- Storing `Optional` in collections or instance fields. (It adds memory overhead and is considered an anti-pattern. Collections should just omit absent keys/values).
