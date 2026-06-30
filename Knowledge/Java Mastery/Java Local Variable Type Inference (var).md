---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 9 — Modern Java Features"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [java, var, type-inference]
---

# Java Local Variable Type Inference (var)

Introduced in Java 10, the `var` keyword allows the compiler to infer the type of a local variable from the right-hand side of the assignment.

## Crucial Distinction
**This is NOT dynamic typing like JavaScript.** The variable's type is fixed and strongly checked at compile time. It's just syntactic sugar to save keystrokes.
```java
var name = "Surya"; // name is strictly a String forever
// name = 42;       // Compile error
```

## When to use `var`
Use it when the type is blindingly obvious from the right-hand side, especially if the explicit type declaration is long and verbose.
```java
// Good
var map = new HashMap<String, List<Order>>();

// Bad - hides type from code reviewer
var result = service.process(); 
```

## Restrictions
`var` can ONLY be used for local variables inside methods. It CANNOT be used for:
- Method parameters
- Class fields
- Variables initialized to `null` (because `null` has no type to infer)
