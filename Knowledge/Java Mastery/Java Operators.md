---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, syntax, operators]
---

# Java Operators

## Arithmetic
- `/` performs **integer division** when both operands are integers. `10 / 3` evaluates to `3`, truncating the decimal. To get `3.33`, cast one operand to `double`: `(double) 10 / 3`.
- `%` (modulus) returns the remainder.

## Logical Operators (Short-Circuiting)
- `&&` (AND): If the left side is `false`, the right side is **never evaluated**.
- `||` (OR): If the left side is `true`, the right side is **never evaluated**.

*Common idiom:* Using short-circuiting to prevent NullPointerExceptions:
```java
if (name != null && name.length() > 0) {
    // If name is null, length() is never called
}
```

## Bitwise Operators
- `&` (AND), `|` (OR), `^` (XOR), `~` (NOT)
- `<<` (Left shift): Shifts bits left (multiplies by 2).
- `>>` (Signed right shift): Shifts bits right, preserving the sign bit (divides by 2).
- `>>>` (Unsigned right shift): Shifts bits right, padding with `0`s regardless of the original sign. Essential for hash calculations and unsigned arithmetic.
