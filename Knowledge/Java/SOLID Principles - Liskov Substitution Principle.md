---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming (OOP)"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["SOLID Principles - Single Responsibility Principle", "SOLID Principles - Open Closed Principle"]
tags: [java, oop, solid, lsp]
---

# SOLID Principles - Liskov Substitution Principle

**Subclasses must be substitutable for their superclass without breaking the program.**

A subclass should honor all the contracts (preconditions, postconditions, invariants) of its superclass. If you pass a subclass object into a method that expects the superclass, the method should continue to function perfectly.

## The Classic Violation: Square extends Rectangle
Mathematically, a square is a rectangle. But in OOP, `Square` breaks `Rectangle`'s contract.
```java
class Rectangle {
    protected int width, height;
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int getArea() { return width * height; }
}

class Square extends Rectangle {
    @Override
    public void setWidth(int w) {
        this.width = w;
        this.height = w; // MUST keep equal
    }
    @Override
    public void setHeight(int h) {
        this.width = h; // MUST keep equal
        this.height = h;
    }
}
```

If a method expects a `Rectangle`:
```java
void testRectangle(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.getArea() == 50; // FAILS if r is a Square (area becomes 100)
}
```

## The Fix
Do not use inheritance here because they are not completely substitutable in behavior. Instead, use an interface `Shape` that both implement, without extending each other.
