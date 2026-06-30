---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, aop, architecture]
---

# Cross-Cutting Concerns

## Intuition
A cross-cutting concern is a piece of behavior that must be applied uniformly across many classes (e.g., logging performance, checking security, opening database transactions).

Without Aspect-Oriented Programming (AOP), you would have to duplicate this infrastructure code inside every single method, cluttering the business logic. 
AOP solves this by separating the "what to do" (the business logic) from the "when and around what to do it" (the cross-cutting concern). It allows you to define advice that is automatically applied to matching methods without those methods knowing anything about it.
