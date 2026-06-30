---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, strings, performance]
---

# StringBuilder and String Concatenation

Because Strings are immutable in Java, concatenating strings in a loop is a massive performance trap.

## The O(n²) Trap
```java
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i; // DANGER!
}
```
In the code above, `result += i` creates a **new String object** every single iteration, copying the entire contents of the previous string into the new one. This results in $O(n^2)$ time complexity and generates enormous amounts of garbage for the GC.

## The Solution: StringBuilder
Always use `StringBuilder` for assembling strings inside loops. It acts as a mutable character array buffer.
```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i); // Modifies the existing buffer (O(1) amortized)
}
String result = sb.toString(); // One final allocation
```
This reduces the time complexity to $O(n)$.

*Note: The Java compiler is smart enough to optimize simple concatenations like `String s = "a" + "b";` into a single literal, but it cannot optimize `+=` inside loops.*
