---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, transactions, aop]
---

# @Transactional (What it actually does)

## Intuition
`@Transactional` guarantees that either everything in a method succeeds and commits together, or nothing commits (no half-finished state). It is implemented via a Spring AOP proxy.

## How the Proxy Works
When a method annotated with `@Transactional` is called from the outside:
1. The proxy intercepts the call.
2. It checks for an active transaction (via a `ThreadLocal`). Depending on the `propagation` setting, it joins it or creates a new one.
3. It delegates to the real method.
4. If the method returns normally: the transaction is **committed**.
5. If the method throws an **unchecked exception** (`RuntimeException` or `Error`): the transaction is **rolled back**.
6. If the method throws a **checked exception**: by default, the transaction **commits**. (You can override this with `rollbackFor = Exception.class`).

*(Note: Because it's implemented via proxy, `@Transactional` only works on public methods, and fails silently on self-invocation).*
