---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, lambda, references]
---

# Java Method References

Method references (`::`) are shorthand syntax for lambdas that simply call an existing method. There are four types:

1. **Static method reference:** `ClassName::staticMethod`
   Equivalent to: `n -> ClassName.staticMethod(n)`
2. **Instance method of a specific instance:** `instance::method`
   Equivalent to: `n -> instance.method(n)`
3. **Instance method of an arbitrary instance:** `ClassName::method`
   The first parameter of the lambda becomes the instance the method is called on.
   `String::toUpperCase` is equivalent to: `s -> s.toUpperCase()`
4. **Constructor reference:** `ClassName::new`
   Equivalent to: `() -> new ClassName()` (or passing arguments if the functional interface demands them).
