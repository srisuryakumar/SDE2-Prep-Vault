---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, lambda, syntax]
---

# Java Lambdas

Lambdas (introduced in Java 8) provide a concise syntax for implementing Functional Interfaces inline, replacing bulky anonymous inner classes.

## Syntax Variations
1. **No arguments:** `() -> System.out.println("Hi")`
2. **One argument:** `s -> s.length()` (Parentheses optional)
3. **Multiple arguments:** `(a, b) -> a + b`
4. **Block body:** 
   ```java
   (a, b) -> {
       int sum = a + b;
       return sum; // Explicit return required inside {}
   }
   ```

## Variable Capture
Lambdas can access variables defined outside their scope, but those variables must be **effectively final** (never reassigned after initialization). If you try to reassign a captured variable, the compiler will throw an error.
