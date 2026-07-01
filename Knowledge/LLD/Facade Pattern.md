---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Adapter Pattern"]
tags: [lld, design-patterns, structural]
---

# Facade Pattern

## Intuition
A complex subsystem has many distinct classes and components (e.g., video decoding, audio extraction, thumbnail generation, S3 uploading). A client shouldn't need to coordinate all of these just to "process a video."

## The Solution
Create a `Facade` class that provides a single, simple, intent-revealing entry point to the subsystem. The Facade orchestrates the complex logic internally, hiding the complexity from the client.

**Facade vs Adapter:**
- Adapter: Makes an existing interface compatible with another.
- Facade: Creates a NEW, simpler interface to a complex subsystem.

**When NOT to use:**
If the client legitimately needs fine-grained control over the individual steps, a Facade is inappropriate because it trades flexibility for simplicity.
