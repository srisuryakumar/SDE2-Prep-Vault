---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, records, data]
---

# Java Records

Introduced in Java 14 and finalized in Java 16, **records** provide a concise syntax for defining immutable data carrier classes (Data Transfer Objects - DTOs).

## The Boilerplate Problem
Before records, a simple class to hold an `id` and `name` required fields, a constructor, getters, `equals()`, `hashCode()`, and `toString()`—often over 40 lines of boilerplate code.

## The Record Solution
```java
public record UserDTO(Long id, String name, String email) {}
```
In one line, the compiler auto-generates:
- `private final` fields for each component.
- A canonical constructor assigning all fields.
- Public accessor methods (`id()`, `name()`, `email()`—note the lack of a "get" prefix).
- Semantic `equals()`, `hashCode()`, and `toString()` methods based on all fields.

## Record Rules
- Records are **immutable**: fields cannot be changed after construction.
- You can define a "compact constructor" for validation without restating the parameters:
  ```java
  public record OrderDTO(Long id, BigDecimal amount) {
      public OrderDTO {
          if (amount.compareTo(BigDecimal.ZERO) < 0) {
              throw new IllegalArgumentException("Negative amount");
          }
      }
  }
  ```
