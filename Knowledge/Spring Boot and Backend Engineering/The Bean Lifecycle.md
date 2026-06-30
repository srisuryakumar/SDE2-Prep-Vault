---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, bean, lifecycle, ioc]
---

# The Bean Lifecycle

## Intuition
The Spring `ApplicationContext` (IoC Container) is responsible for creating, wiring, and destroying objects (beans) in a specific order.

## The Sequence
1. **Instantiation**: The container calls the bean's constructor.
2. **Dependency Injection**: The container injects dependencies (via constructor, setter, or field).
3. **`Aware` callbacks**: If the bean implements `ApplicationContextAware` or `BeanNameAware`, those setters are called.
4. **`BeanPostProcessor#postProcessBeforeInitialization`**: A hook that runs on every bean before initialization.
5. **`@PostConstruct`**: The bean's own initialization logic. Guaranteed to run *after* dependency injection is complete. Perfect for warming caches or opening connections.
6. **`BeanPostProcessor#postProcessAfterInitialization`**: This is where **Spring AOP proxies** get created. If a bean has `@Transactional`, it gets wrapped in a proxy here, and the container hands out the proxy instead of the real bean.
7. **Ready for use**: The bean sits in the container for the lifetime of the application.
8. **`@PreDestroy`**: Called when the context shuts down, to release resources.

## Interview Strategy
> "What's the difference between doing setup work in a constructor vs `@PostConstruct`?"

**Answer:** A constructor can only safely use what is passed as its own parameters. It has no guarantee that the broader application context is ready. `@PostConstruct` runs strictly *after* all of the bean's dependencies are injected, making it the safe place to call methods on those injected dependencies (e.g., calling an injected service to prime a cache). It separates "building the object" from "the object is ready to do work".
