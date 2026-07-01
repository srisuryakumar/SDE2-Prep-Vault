---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["The Self-Invocation Trap (Spring AOP)"]
tags: [spring, aop]
---

# Spring AOP Proxy Model

## Intuition
Unlike full AspectJ (which modifies bytecode at compile-time), Spring AOP is **proxy-based**. It wraps Spring-managed beans in proxy objects at runtime.

## The Sequence
1. Spring instantiates your real bean (e.g. `OrderService`).
2. A `BeanPostProcessor` inspects it to see if any AOP pointcuts match its methods.
3. If there is a match, Spring creates a proxy object.
4. The proxy is registered in the `ApplicationContext`. Other beans inject the proxy, not the real instance.
5. When `OrderController` calls `orderService.createOrder()`, it calls the proxy. The proxy runs the advice (e.g. opens a transaction), delegates to the real `createOrder()` method on the target instance, and then runs the post-call advice.

## Connection to the Self-Invocation Trap
This fully explains why `@Transactional` and other AOP annotations fail on self-invocation. When `OrderService.createOrder()` calls `this.someOtherMethod()`, the call is made directly on the real object instance (`this`), bypassing the proxy entirely. The proxy never intercepts the call, so the advice never runs.
