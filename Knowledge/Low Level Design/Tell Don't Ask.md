---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [oop, design-principles]
---

# Tell Don't Ask

## Intuition
Tell an object what to do rather than asking it for data and doing the computation yourself.

## Procedural vs Object-Oriented
**Asking (Procedural):** Extracting data from an object via getters, reasoning about it in an external service, and acting on it. This leaks business logic into external services.
```java
// Bad: Asking
if (order.getStatus() == PENDING && !order.getItems().isEmpty()) {
    order.setStatus(PROCESSING);
}
```

**Telling (OOP):** The logic lives where the data lives. You just call a method.
```java
// Good: Telling
order.process();
```

**Smell Detector:** Every time you write `if (object.getSomething() == X)` outside the object, ask yourself if that condition should be encapsulated *inside* the object itself.
