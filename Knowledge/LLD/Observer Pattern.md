---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, behavioral]
---

# Observer Pattern (Event Bus)

## Intuition
When multiple downstream services need to react to something happening in an upstream service, you want to avoid direct coupling (where the upstream service directly calls the downstream services).

## The Solution
Use an Event Bus or Publisher-Subscriber model.
- **Publisher (Subject):** When something happens, it constructs an Event object (`OrderPlacedEvent`) and publishes it to the Event Bus. It has NO IDEA who is listening.
- **Subscriber (Observer):** Registers its interest in specific Event types with the Event Bus. When an event is published, the subscriber's handler method is invoked.

**Real-world Examples:**
- Spring's `@EventListener` and `ApplicationEventPublisher`.
- Kafka (at scale, distributed and durable).

**Benefits:**
- Perfect adherence to Open-Closed Principle: You can add 10 new subscribers without touching the publisher's code once.
