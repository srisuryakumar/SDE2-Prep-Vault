---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 3 — Spring Boot Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, dependency-injection, ioc]
---

# Dependency Injection (Constructor vs Field vs Setter)

## Intuition
Spring supports three ways to inject dependencies. Constructor injection is the only correct default.

## 1. Field Injection
```java
@Autowired
private OrderRepository orderRepository;
```
**Cons:** The field is mutable. If `OrderRepository` can't be resolved, the class still constructs fine, but throws an NPE later in production when you try to use it. Hard to test without Spring.

## 2. Setter Injection
```java
@Autowired
public void setOrderRepository(OrderRepository repo) { this.repo = repo; }
```
Used for optional dependencies.

## 3. Constructor Injection (The Recommended Default)
```java
private final OrderRepository orderRepository;

public OrderService(OrderRepository orderRepository) {
    this.orderRepository = orderRepository;
}
```
*(Often generated using Lombok's `@RequiredArgsConstructor`)*

**Why Constructor Injection is Best:**
1. **Immutability:** Dependencies can be `final`.
2. **Fail Fast:** If a dependency is missing, the application fails to start immediately (at construction time), rather than throwing an NPE in production later.
3. **Testability:** You can easily unit test the class with `new OrderService(mockRepo)` without needing the Spring container.
4. **Circular Dependencies:** Surfaced immediately at startup (`BeanCurrentlyInCreationException`), forcing you to fix bad architectural boundaries, instead of silently being papered over by field injection.
