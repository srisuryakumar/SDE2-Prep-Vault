---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, classes, objects]
---

# Java Classes and Objects

- A **class** is a blueprint defining fields (state) and methods (behavior).
- An **object** (instance) is a concrete entity created from that blueprint, residing on the Heap.

## Constructors
Constructors are special methods invoked when an object is created via the `new` keyword. They must have the exact same name as the class and **no return type** (not even `void`).

## The `this` Keyword
`this` is a reference to the **current object instance** on which a method is invoked.
It is primarily used to:
1. Distinguish between instance fields and method parameters with the same name.
   ```java
   public void setCount(int count) {
       this.count = count; // 'this.count' is the field, 'count' is the parameter
   }
   ```
2. Call another constructor in the same class: `this(0);`
3. Return the current object for method chaining (builder pattern): `return this;`
