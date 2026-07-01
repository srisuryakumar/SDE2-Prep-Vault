---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, enums, oop]
---

# Java Enums

In many languages, enums are just a set of named integers. In Java, **Enums are full-featured classes**.

## Fields, Constructors, and Methods
An enum can hold state and behavior just like a regular class. Each enum constant is essentially a singleton instance of the enum class.
```java
public enum Planet {
    EARTH(5.976e+24, 6.37814e6),
    MARS(6.421e+23, 3.3972e6); // Enum instances
    
    private final double mass;
    private final double radius;
    
    // Enum constructors are implicitly private
    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }
    
    public double surfaceGravity() {
        return (6.67300E-11) * mass / (radius * radius);
    }
}
```

## Abstract Methods in Enums
You can declare an `abstract` method in an enum, forcing each constant to provide its own implementation.
```java
public enum Operation {
    PLUS { public int apply(int x, int y) { return x + y; } },
    MINUS { public int apply(int x, int y) { return x - y; } };
    
    public abstract int apply(int x, int y);
}
```

## Useful Built-in Methods
- `Direction.values()`: Returns an array of all constants.
- `Direction.valueOf("NORTH")`: Converts a String to the enum constant (throws exception if not found).
- `Direction.NORTH.ordinal()`: Returns the zero-based index of the constant's declaration.
