---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, strings, memory]
---

# String Immutability and the String Pool

`String` is a class in Java (`java.lang.String`), but it behaves uniquely.

## Immutability
Once a String object is created, it cannot be modified. Operations like `.toUpperCase()` or concatenation (`+`) do not modify the original String; they return a **new** String object.
- **Why?** Thread safety, security (cannot modify a validated SQL query string), and it enables the String Pool.

## The String Pool
Java maintains a special area in the Heap called the String Pool to save memory. 
When you declare a string literal (`"hello"`), the JVM checks the pool. If "hello" is already there, it returns the existing reference. If not, it creates a new object in the pool.

```java
String a = "hello"; // Creates in pool
String b = "hello"; // Reuses pool reference
System.out.println(a == b); // true (same object)

String c = new String("hello"); // Bypasses pool, creates NEW object on Heap
System.out.println(a == c); // false (different objects)
```

## `==` vs `.equals()`
- `==` compares **memory addresses** (are these the exact same object?).
- `.equals()` compares **content** (do these objects contain the same characters?).

For Strings (and all objects), **always use `.equals()`**.
```java
// BEST PRACTICE: null-safe comparison
if ("yes".equals(userInput)) { ... } // Won't throw NPE if userInput is null
```
