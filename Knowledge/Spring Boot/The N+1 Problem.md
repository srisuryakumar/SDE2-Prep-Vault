---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, performance, database]
---

# The N+1 Problem

## Intuition
The N+1 problem is the most common performance issue in JPA. It happens when you load a list of `N` parent entities (1 query) and then access a lazy association on each of them, triggering `N` additional queries.
Total queries = N + 1. For 1,000 orders, that's 1,001 queries.

## Example
```java
List<Order> orders = orderRepository.findAll();  // Query 1
return orders.stream()
    .map(o -> o.getUser().getEmail())            // Queries 2 through N+1
    .toList();
```
When `findAll` runs, `Order.user` is populated with a *proxy*. When `.getUser().getEmail()` is called, Hibernate materializes the proxy by firing a `SELECT` against the `users` table for that specific `id`. It fires a query *per order*, even if the user is the same.

## How to Detect It
Turn on `spring.jpa.show-sql=true`. If you see the exact same `SELECT` statement (e.g. `WHERE user_id = ?`) repeated dozens of times in the console logs during a single request, you have an N+1 problem.

## How to Fix It
1. **`JOIN FETCH`**: For custom JPQL queries.
2. **`@EntityGraph`**: For derived query methods.
3. **`@BatchSize`**: For deeply nested code where changing queries is hard.
