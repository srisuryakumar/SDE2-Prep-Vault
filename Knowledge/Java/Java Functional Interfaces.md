---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, functional, interfaces, lambda]
---

# Java Functional Interfaces

A **Functional Interface** is any interface that has exactly **one abstract method**. It is the foundation that enables Lambda expressions in Java.

## The `@FunctionalInterface` Annotation
This annotation is optional but recommended. It tells the compiler to enforce the "single abstract method" rule, preventing someone from accidentally adding a second abstract method later and breaking all lambdas implementing it. Default methods do not count toward this limit.

## The Core Functional Interfaces (`java.util.function`)
1. **`Predicate<T>`**: `T -> boolean`. Takes an argument, evaluates a condition, returns true/false. (Used in `filter()`)
2. **`Function<T, R>`**: `T -> R`. Takes an argument, transforms it, returns a result. (Used in `map()`)
3. **`Consumer<T>`**: `T -> void`. Takes an argument, does something (like print), returns nothing. (Used in `forEach()`)
4. **`Supplier<T>`**: `() -> T`. Takes no arguments, returns a new or generated value.
5. **`UnaryOperator<T>`**: `T -> T`. A specialized `Function` where the input and output types are identical.
6. **`BinaryOperator<T>`**: `(T, T) -> T`. A specialized `BiFunction` where inputs and output are all the same type. (Used in `reduce()`)
