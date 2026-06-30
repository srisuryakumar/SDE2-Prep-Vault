---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# Integer Overflow and Floating Point

## Signed and Unsigned Integers
- **Unsigned integers:** Store only non-negative values. (e.g., 8-bit unsigned: 0 to 255).
- **Signed integers (two's complement):** The most significant bit indicates sign (0=positive, 1=negative). E.g., an 8-bit signed range is -128 to +127.

### Integer Overflow
A 32-bit signed integer holds values from -2,147,483,648 to +2,147,483,647. Adding 1 to the maximum value wraps it around to the minimum negative value.

```java
int max = Integer.MAX_VALUE;  // 2,147,483,647
int overflow = max + 1;       // -2,147,483,648  ← wraps to negative!
```
To prevent this, use `long` (64-bit) for large values, or methods like `Math.addExact()` in Java which throw an `ArithmeticException` on overflow rather than silently wrapping.

## Floating-point numbers (IEEE 754)
Real numbers cannot be stored as exact integers. The CPU uses a scientific-notation-like format: `sign bit + exponent + mantissa`.

This means decimal fractions like 0.1 have no exact binary representation, leading to precision issues:
```javascript
0.1 + 0.2 === 0.3  // false — gives 0.30000000000000004
```

> [!WARNING]
> **Never use float/double for money.** Use `BigDecimal` in Java or store values as integer cents (e.g., $12.99 stored as `1299` cents).
