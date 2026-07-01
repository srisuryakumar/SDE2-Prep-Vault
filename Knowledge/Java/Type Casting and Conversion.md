---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, syntax, casting]
---

# Type Casting and Conversion

In Java, assigning a value of one primitive type to a variable of another type involves casting.

## Widening (Implicit Casting)
Moving from a smaller data type to a larger one is safe. The compiler does it automatically without data loss.
`byte → short → int → long → float → double`

```java
int i = 100;
long l = i; // Automatic widening
```

## Narrowing (Explicit Casting)
Moving from a larger type to a smaller type risks data loss (truncation). The compiler forces you to write an explicit cast `(type)` to prove you know what you are doing.

```java
double pi = 3.14159;
int approx = (int) pi; // Explicit cast. Truncates to 3.

int large = 300;
byte b = (byte) large; // OVERFLOW! 300 doesn't fit in a byte. 
// Result is 44 (the lower 8 bits of 300).
```
