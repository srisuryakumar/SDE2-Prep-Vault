---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["@Transactional (What it actually does)"]
tags: [spring, aop, transactions]
---

# How @Transactional is implemented

## Intuition
`@Transactional` is fully implemented as a Spring AOP proxy using an `@Around` advice called `TransactionInterceptor`.

## The Execution Flow
1. `TransactionInterceptor`'s pointcut matches any method annotated with `@Transactional`.
2. When the proxy is called, `TransactionInterceptor.invoke()` runs:
   - It checks the `propagation` attribute (e.g. `REQUIRED`, `REQUIRES_NEW`).
   - It obtains a database connection (joining an existing `ThreadLocal` one, or fetching a new one from HikariCP and setting `autoCommit=false`).
   - It calls `pjp.proceed()`, executing the real business method.
   - If the method returns normally, it calls `connection.commit()`.
   - If the method throws an exception matching the rollback rules (by default, unchecked exceptions like `RuntimeException` and `Error`), it calls `connection.rollback()`.

Understanding this completely explains why self-invocation fails (proxy is bypassed) and what `readOnly = true` does (sets connection to read-only and skips Hibernate dirty checking).
