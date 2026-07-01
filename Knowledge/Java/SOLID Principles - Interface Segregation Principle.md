---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming (OOP)"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["SOLID Principles - Single Responsibility Principle"]
tags: [java, oop, solid, isp]
---

# SOLID Principles - Interface Segregation Principle

**Clients should not be forced to depend on interfaces they don't use.**

"Fat" interfaces break cohesion and force implementing classes to provide dummy implementations for methods they don't care about.

## The Violation
```java
interface Animal {
    void eat();
    void fly(); // Dogs can't fly!
    void swim(); // Eagles don't swim!
}

class Dog implements Animal {
    public void eat() { ... }
    public void fly() { throw new UnsupportedOperationException(); } // BAD
    public void swim() { ... }
}
```

## The Fix
Segregate into small, focused interfaces.
```java
interface Eatable { void eat(); }
interface Flyable { void fly(); }
interface Swimmable { void swim(); }

class Dog implements Eatable, Swimmable {
    // Only implements what it can actually do
}
```
