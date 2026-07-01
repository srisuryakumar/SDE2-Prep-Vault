---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 8 — Spring AOP"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, aop]
---

# @Around and proceed()

## Intuition
`@Around` is the most powerful AOP advice type because it controls the *entire* lifecycle of the method invocation, much like a servlet Filter.

## How it works
An `@Around` method takes a `ProceedingJoinPoint`.
```java
@Around("somePointcut()")
public Object advice(ProceedingJoinPoint pjp) throws Throwable {
    // 1. BEFORE logic
    Object result;
    try {
        result = pjp.proceed(); // 2. THE REAL METHOD RUNS
    } catch (Exception e) {
        // 3. ON EXCEPTION
        throw e;
    }
    // 4. AFTER RETURNING
    return result; 
}
```

## The Power of proceed()
`pjp.proceed()` is what actually triggers the target method.
- **Caching:** If you check a cache and find a hit, you can return the cached value directly and *never call `proceed()`*, completely suppressing the actual method execution (this is how `@Cacheable` works).
- **Argument Modification:** You can pass modified arguments via `pjp.proceed(newArgs)`.
