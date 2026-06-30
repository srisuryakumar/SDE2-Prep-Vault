---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 9 — Modern Java Features"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, pattern-matching, instanceof]
---

# Java Pattern Matching for instanceof

Introduced in Java 16, pattern matching for `instanceof` eliminates the need for manual casting after checking an object's type.

## The Old Way
```java
if (obj instanceof String) {
    String s = (String) obj; // Redundant manual cast
    System.out.println(s.length());
}
```

## The New Way
You can declare a pattern variable (`s`) right inside the `instanceof` check. If the check succeeds, the variable is automatically bound and casted.
```java
if (obj instanceof String s) {
    System.out.println(s.length()); // 's' is already a String
}
```

## Flow Scoping
The pattern variable is in scope only where the compiler can guarantee the check succeeded.
```java
// Works inside an && condition
if (obj instanceof String s && s.length() > 5) { ... }

// DOES NOT work inside an || condition
if (obj instanceof String s || s.length() > 5) { ... } // Error: 's' might not be bound

// Works AFTER the if block if the if block throws or returns
if (!(obj instanceof String s)) {
    return;
}
System.out.println(s.length()); // 's' is in scope here because we only reach here if obj IS a String
```
