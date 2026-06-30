---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 3 — Java Syntax from Scratch"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [java, syntax, primitives]
---

# Java Variables and Primitive Types

Unlike JavaScript where everything is an object, Java separates primitive types from objects. Primitives are raw values stored directly in memory (on the Stack for local variables, or inside the object on the Heap for fields).

## The 8 Primitive Types
- `byte` (8 bits, -128 to 127)
- `short` (16 bits)
- `int` (32 bits, ~±2.1 billion)
- `long` (64 bits, requires `L` suffix: `100L`)
- `float` (32 bits, requires `f` suffix: `3.14f`)
- `double` (64 bits, default for decimals)
- `char` (16 bits, single quotes: `'A'`)
- `boolean` (`true` or `false` only; NOT an integer like in C)

*Note: Never use `float` or `double` for currency calculations due to IEEE 754 precision issues (e.g. `0.1 + 0.2 != 0.3`). Use `java.math.BigDecimal`.*

## Variable Rules
- Local variables (inside methods) MUST be initialized before use.
- Class fields are automatically initialized to default values (`0`, `false`, `\u0000`, `null`).

## Naming Conventions
- Variables/Methods: `camelCase`
- Classes/Interfaces: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
