---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, structural, performance]
---

# Flyweight Pattern

## Intuition
When creating massive numbers of fine-grained objects that share most of their state, the JVM heap will overflow. The Flyweight pattern shares immutable state to save memory.

## Intrinsic vs Extrinsic State
In a text editor rendering 1 million characters, creating a `FontConfig("Arial", 12)` object for every character uses 200MB.
- **Intrinsic State (Shared):** The font name, size, and color. This is identical for millions of characters. We create *one* `FontConfig` object and share it.
- **Extrinsic State (Unique):** The X/Y position of the character. This is passed in as a method parameter during rendering, not stored in the shared object.

## Implementation
Usually implemented via a Factory with a cache (e.g., `ConcurrentHashMap`). The Factory checks if a `FontConfig` with the requested properties exists; if so, it returns the cached reference.

**Real-world Example:** The Java `String` pool is a flyweight cache.
