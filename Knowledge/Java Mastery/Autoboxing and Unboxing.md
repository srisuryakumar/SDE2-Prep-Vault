---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, primitives, objects, autoboxing]
---

# Autoboxing and Unboxing

Java provides **wrapper classes** (`Integer`, `Double`, `Boolean`, etc.) for each primitive type. You must use wrapper classes when using Generics (e.g., `List<Integer>`, not `List<int>`) or when a value can be `null`.

## Autoboxing
The compiler automatically converts a primitive to its wrapper class.
```java
List<Integer> list = new ArrayList<>();
list.add(5); // Autoboxing: compiler inserts Integer.valueOf(5)
```

## Unboxing
The compiler automatically extracts the primitive from the wrapper.
```java
int sum = list.get(0) + 1; // Unboxing: compiler inserts list.get(0).intValue()
```

## The Performance Cost
Autoboxing inside a hot loop is very slow because it allocates a new object on the Heap for every iteration (creating garbage for the GC). Use primitive arrays (`int[]`) for number crunching instead of `List<Integer>`.

## The Null Trap
Unboxing a `null` reference throws a `NullPointerException`.
```java
Integer nullableInt = null;
int i = nullableInt; // Throws NullPointerException!
```
