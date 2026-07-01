---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, boot, configuration, properties]
---

# @Value vs @ConfigurationProperties

## Intuition
Both pull values out of the merged `Environment` into your code.

## @Value
Injects a single property into a single field using SpEL (Spring Expression Language).
```java
@Value("${app.max-items:25}")
private int maxItems;
```
- **Cons:** No compile-time checks for typos in property names. Hard to document all properties in one place. Cannot bind complex nested structures.

## @ConfigurationProperties
Binds an entire group of related properties into a typed, structured object (like a Java Record or POJO).
```java
@ConfigurationProperties(prefix = "app")
public record AppProperties(int maxItems, String supportEmail) {}
```
- **Pros:** Compile-time checked, IDE autocompletion, centrally documented. Uses Spring Boot's `Binder` API to map nested structures, lists, and maps. Uses "relaxed binding" so `kebab-case` in YAML maps seamlessly to `camelCase` in Java.
- **When to use:** Use `@Value` for a one-off property. Use `@ConfigurationProperties` the moment you have more than two related settings.
