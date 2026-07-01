---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, applicationcontext, beanfactory]
---

# ApplicationContext vs BeanFactory

## Intuition
- **`BeanFactory`**: The root interface. The most basic DI container (holds definitions and produces beans lazily on request).
- **`ApplicationContext`**: Extends `BeanFactory`. Adds application framework features: event publishing (`ApplicationEventPublisher`), I18N (`MessageSource`), the `Environment` abstraction (profiles and properties), and AOP integration.

## Eager Initialization
Most importantly, `ApplicationContext` **eagerly initializes singletons by default**. Every singleton bean is constructed at startup, not lazily on first use. 
This is a deliberate fail-fast design: if a bean is broken (missing property, unsatisfiable dependency), the app fails to start immediately, rather than failing hours later in production when a request happens to hit it.
If you have a very expensive bean that is rarely used, you can use `@Lazy` to opt it out of eager initialization.
