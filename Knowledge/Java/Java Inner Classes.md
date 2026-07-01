---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [java, classes, syntax]
---

# Java Inner Classes

Java allows defining classes inside other classes. There are three primary types:

## 1. Static Nested Class
Belongs to the outer class itself, not to an instance. It does NOT hold a reference to the outer instance, meaning it cannot access the outer class's instance fields.
```java
public static class StaticNested { ... }
// Instantiated via: new Outer.StaticNested();
```

## 2. Inner Class (Non-Static)
Belongs to an *instance* of the outer class. Every instance of an Inner class implicitly holds a reference to the Outer instance that created it. It can access all members of the outer class, including private ones.
```java
public class Inner { ... }
// Instantiated via: outerInstance.new Inner();
```

## 3. Anonymous Class
An inline implementation of an interface or abstract class. It has no name and is instantiated exactly where it is defined. Often replaced by Lambdas in modern Java.
```java
Runnable r = new Runnable() {
    @Override
    public void run() { System.out.println("Running"); }
};
```
