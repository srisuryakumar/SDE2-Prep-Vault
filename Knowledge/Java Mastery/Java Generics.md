---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 6 — Generics and Functional Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, generics, types, erasure]
---

# Java Generics

Generics (introduced in Java 5) provide **compile-time type safety** and eliminate the need for manual casting when retrieving objects from collections.

## Why Generics Exist
Before generics, collections stored raw `Object` references. You could add an `Integer` to a list meant for `String`s, and the compiler wouldn't complain. The program would crash with a `ClassCastException` at runtime when you tried to cast the retrieved element back to a `String`. Generics move this error from runtime to compile time.

## Generic Classes and Methods
- **Class:** `public class Box<T> { private T content; }`
- **Method:** `public static <T> T max(T a, T b)`
Common type parameter names: `T` (Type), `E` (Element), `K` (Key), `V` (Value).

## Bounded Type Parameters
You can restrict the types that can be used:
- `T extends Number`: T must be a subclass of Number (or Number itself).
- `T extends Comparable<T>`: T must implement the Comparable interface.

## Type Erasure
Java generics are a compile-time construct. At runtime, the JVM knows nothing about them (this is called **Type Erasure**).
- `List<String>` and `List<Integer>` both become just `List` at runtime.
- Because of this, you cannot do `new T()` or `if (obj instanceof T)` inside generic code.
