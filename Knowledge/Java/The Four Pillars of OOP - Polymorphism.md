---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, polymorphism, vtable]
---

# The Four Pillars of OOP - Polymorphism

Polymorphism means "many forms." It allows objects of different types to be treated as instances of the same class through a common interface.

## Compile-Time Polymorphism (Method Overloading)
Having multiple methods with the **same name but different parameters**. The compiler decides which method to call at compile time based on the argument types (Static Dispatch).

## Runtime Polymorphism (Method Overriding & Late Binding)
A subclass overriding a parent method. 
If a parent reference variable points to a child object (`Animal a = new Dog()`), invoking a method (`a.makeSound()`) will execute the child's overridden version.

**How does the JVM know? (The vtable)**
Every class has a virtual method table (vtable) in Metaspace. At runtime, when `a.makeSound()` is called:
1. The JVM checks the *actual* object type on the Heap (it sees `Dog`).
2. It looks up `Dog`'s vtable.
3. It finds that `makeSound` points to `Dog.makeSound()`, and calls it.
This is known as **dynamic dispatch** or **late binding**.

## The `instanceof` Operator
Used to check if an object is an instance of a specific type before casting. 
*Java 16+ Pattern Matching:* You can check and cast in one step:
```java
if (shape instanceof Circle c) {
    System.out.println(c.radius()); // 'c' is already cast to Circle
}
```
