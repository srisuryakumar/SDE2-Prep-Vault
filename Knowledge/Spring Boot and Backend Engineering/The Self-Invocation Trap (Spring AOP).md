---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, aop, transactions, gotcha]
---

# The Self-Invocation Trap (Spring AOP)

## Intuition
**`@Transactional` (and any other Spring AOP annotation) has NO EFFECT when one method calls another method in the same class.**

## The Failure Mode
```java
@Service
public class OrderService {
    
    @Transactional
    public void createOrder() {
        sendEmail(); // ← Calling an internal method directly
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void sendEmail() { 
        // INTENT: run in a new transaction.
        // REALITY: the annotation is ignored. It runs in createOrder's transaction.
    }
}
```

## Why?
Spring AOP works by wrapping your bean in a proxy. External callers talk to the proxy, which intercepts the call and starts the transaction. 
But when `createOrder` calls `sendEmail` internally, it calls it on `this` (the real object instance), bypassing the proxy entirely. The proxy never sees the call, so the AOP logic never runs.

## The Fix
**Extract to a separate bean.** Move `sendEmail` to a `NotificationService` bean, inject it into `OrderService`, and call `notificationService.sendEmail()`. The call will go through the `NotificationService` proxy, and the `@Transactional` annotation will be honored.
