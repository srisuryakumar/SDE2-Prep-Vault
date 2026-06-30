---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 9 — Modern Java Features"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [java, text-blocks, strings]
---

# Java Text Blocks

Introduced in Java 15, Text Blocks (`"""`) provide a way to write multi-line string literals without the nightmare of escape characters and `\n` concatenations.

## Syntax
```java
String json = """
    {
      "name": "Surya",
      "role": "Engineer"
    }
    """;
```

## Features
- **Incidental Indentation:** The compiler automatically determines the baseline indentation (based on the position of the closing `"""` or the leftmost character) and strips that common leading whitespace from every line.
- **No Escaping Quotes:** You can use double quotes `"` freely inside the block without escaping them.
- **Trailing Whitespace:** Automatically stripped unless you use the `\s` escape sequence.
- **Line Continuation:** Ending a line with `\` prevents a newline character from being inserted there.
