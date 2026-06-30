---
type: concept
subject: Career Strategy
source_book: "Book 9 — Interview Mastery and Career Strategy"
source_chapter: "Chapter 10 — System Design Interview Strategy"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [career, interview, system-design, strategy]
---

# System Design Interview Strategy

## The 45-Minute Framework
- **Requirements (5 min):** Functional and non-functional requirements, explicit scope.
- **Estimation (5 min):** Back-of-the-envelope scale numbers (QPS, storage, bandwidth).
- **High-level Design (10 min):** Major components and data flow.
- **Deep Dive (15 min):** Deep dive into 1-2 components (often the data model or consistency strategy).
- **Trade-offs & Wrap-up (10 min):** Bottlenecks, failure modes, what you'd revisit.

## Driving the Conversation
Treat the interviewer as a client and yourself as the architect. Check in periodically: "Before I go further, does this high-level approach match what you had in mind, or should I explore a different direction?"

## How to Present Trade-offs
Use this structure: "I chose **[X]** because **[reason tied to requirements]**, the downside is **[Y]**, and I'd mitigate that with **[Z]**."
*Example:* "I chose eventual consistency for the like-count because strict consistency adds latency to every read... the downside is a stale count, mitigated by converging within a few seconds via the event stream."

## Common Mistakes
- **Not scoping:** Diving in without agreeing on what's in scope.
- **Over-engineering:** Reaching for Kafka/sharding when the scale doesn't demand it.
- **Ignoring non-functional requirements:** Designing only for "it works" without addressing availability/latency.

## Handling the Unknown
If asked to design something you don't know: "I haven't worked with this specific type of system before, so let me reason through it from the core requirements — what does it need to do, at what scale..." First-principles reasoning outperforms guessing.
