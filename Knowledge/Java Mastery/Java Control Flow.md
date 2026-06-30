---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, syntax, control-flow]
---

# Java Control Flow (Switch Expressions and Loops)

## Switch Expressions (Java 14+)
Modern Java uses **arrow syntax (`->`)** for switch expressions, which prevents accidental fall-through bugs and ensures exhaustiveness.

```java
// Arrow syntax — no 'break' needed
String dayName = switch (day) {
    case 1 -> "Monday";
    case 2, 3, 4, 5 -> "Weekday"; // Multiple labels
    case 6, 7 -> "Weekend";
    default -> {
        System.out.println("Invalid day");
        yield "Unknown"; // 'yield' returns a value from a block
    }
};
```

## Loops
- `while`, `do-while`, and traditional `for` loops behave identically to C/JavaScript.
- **Enhanced for-each loop:** Iterates over arrays or `Iterable` collections. The iteration variable is a read-only copy of the value/reference.
  ```java
  for (String name : names) { ... }
  ```

## Labeled Break and Continue
You can break or continue an **outer** loop from within an **inner** loop using labels:
```java
outer:
for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
        if (i == 2 && j == 3) break outer; // Breaks the 'outer' loop entirely
    }
}
```
