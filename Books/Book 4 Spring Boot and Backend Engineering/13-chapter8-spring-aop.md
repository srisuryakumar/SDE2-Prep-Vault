# Chapter 8: Spring AOP and Cross-Cutting Concerns

## 8.1 What AOP solves

A **cross-cutting concern** is a piece of behavior that must be applied uniformly across many classes — not because those classes share the same domain purpose, but because they all need the same surrounding infrastructure. Logging how long every service method takes, collecting metrics on every repository call, checking security before every controller method runs, opening and closing a transaction around every public service method — these all fit the pattern.

Without AOP, you'd implement these concerns by hand in each class:

```java
// Without AOP — duplicated in every service method:
public OrderResponse createOrder(CreateOrderRequest request) {
    long start = System.currentTimeMillis();
    log.debug("createOrder called with {} items", request.items().size());
    try {
        // ... actual business logic ...
        long elapsed = System.currentTimeMillis() - start;
        log.debug("createOrder completed in {}ms", elapsed);
        return response;
    } catch (Exception e) {
        log.error("createOrder failed after {}ms", System.currentTimeMillis() - start, e);
        throw e;
    }
}
```

Multiply this across every method in every service class, and you have two problems: every method is cluttered with infrastructure code that obscures the actual business logic, and changing the logging format requires editing every method individually.

AOP separates the "what to do" (the business logic) from the "when and around what to do it" (the cross-cutting concern), by allowing you to define advice that is automatically applied to matching methods — without those methods knowing anything about it.

## 8.2 How Spring AOP works: the proxy model

Spring AOP (in contrast to full AspectJ) is **proxy-based**. It doesn't modify bytecode or weave aspects at compile time — it wraps Spring-managed beans in proxy objects at runtime, during the bean lifecycle (specifically, at step 6 of the lifecycle from Chapter 3 — `BeanPostProcessor#postProcessAfterInitialization`).

Here's the concrete sequence:

1. Spring discovers `OrderService` via component scanning and instantiates the real `OrderService` object.
2. A `BeanPostProcessor` (specifically, `AbstractAutoProxyCreator`) inspects the freshly built `OrderService` and checks whether any aspect's pointcut matches any of its methods.
3. If there's a match (e.g., a performance-logging aspect that targets all methods in `..service..*`), Spring creates a **proxy** — either a JDK dynamic proxy (if `OrderService` implements an interface) or a CGLIB-generated subclass proxy (the default for concrete classes without an interface, which is our case).
4. The proxy is what gets registered in the `ApplicationContext` and what every other bean that injects `OrderService` actually receives. The real `OrderService` instance lives inside the proxy, as its "target."
5. When `OrderController` calls `orderService.createOrder(...)`, it calls the **proxy's** `createOrder()`. The proxy runs the configured advice (opens a transaction, starts a timer, etc.), then delegates to the real `OrderService.createOrder()`, then runs post-call advice (commits, records elapsed time, etc.).

This is also the complete explanation of **why self-invocation breaks `@Transactional`** (and every other AOP-based annotation): when `OrderService.createOrder()` calls `this.somethingElse()`, it's calling the method on the real instance — `this`, not the proxy. The proxy is never involved. Chapter 4 gave you the fix (separate class); now you understand why the fix works: putting the second method on a separate Spring-managed bean means a call to it goes through *that bean's* proxy, which *does* intercept it.

## 8.3 AOP vocabulary

**Aspect** — the class that contains advice; the unit of modularization for a cross-cutting concern. Annotated with `@Aspect`.

**Advice** — code that runs at a specific point. Four main kinds:
- `@Before` — runs before the matched method executes
- `@AfterReturning` — runs after the method returns normally
- `@AfterThrowing` — runs after the method throws an exception
- `@After` — runs after the method finishes, whether normally or with an exception (like `finally`)
- `@Around` — wraps the entire method call; can run code before and after, inspect/modify the return value or exception, or suppress the call entirely. The most powerful and most commonly used.

**Pointcut** — a predicate that selects which methods the advice applies to. Written as an expression in AspectJ's pointcut language, matched against method signatures at runtime.

**Join point** — a specific method invocation that matched a pointcut. In Spring AOP (proxy-based), only method calls are join points — there's no "field access" or "constructor call" join point, unlike full AspectJ.

**ProceedingJoinPoint** — the object passed to an `@Around` advice, representing the actual method invocation. Calling `proceedingJoinPoint.proceed()` is what actually invokes the target method; not calling it suppresses the invocation entirely (useful for caching, where you return a cached result without calling the real method).

## 8.4 Pointcut expressions

The AspectJ pointcut language is expressive enough to be concise but unfamiliar enough to be tricky the first time. There are five types you'll actually encounter, and mastering all five — plus how to combine them — is what separates a surface-level understanding from a genuinely useful one:

```java
// ─── The 5 Types of Pointcut Expressions ─────────────────────────────────────

@Aspect
@Component
@Slf4j
public class ComprehensiveAspect {

    // TYPE 1: execution() — Match by method signature
    // Syntax: execution([modifier] [return-type] [class].[method]([params]))
    // Most common and most flexible pointcut type

    // Match ANY method in the service package (any class, any method, any args):
    @Pointcut("execution(* dev.surya.orderapi.service.*.*(..))")
    public void anyServiceMethod() {}

    // Match methods named "find*" returning any type in any class:
    @Pointcut("execution(* find*(..))")
    public void anyFindMethod() {}

    // Match only public methods in OrderService with a Long first argument:
    @Pointcut("execution(public * dev.surya.orderapi.service.OrderService.*(Long, ..))")
    public void orderServiceLongArg() {}

    // execution() anatomy:
    // execution( *                              any return type
    //            dev.surya.orderapi.service.    package (. = one level, .. = any depth)
    //            *.                             any class
    //            *(                             any method name
    //            ..))                           any arguments (. = one arg, .. = any number)

    // TYPE 2: @annotation() — Match by annotation on the method
    // Most precise: only methods you explicitly annotate are intercepted

    @Pointcut("@annotation(dev.surya.orderapi.annotation.LogPerformance)")
    public void annotatedWithLogPerformance() {}

    // Usage: place @LogPerformance on any method to activate the aspect
    // @LogPerformance
    // public Order createOrder(CreateOrderDTO dto) { ... }

    // TYPE 3: within() — Match all methods within a type or package
    // Simpler than execution() when you want ALL methods in a class/package

    @Pointcut("within(dev.surya.orderapi.service..*)")  // .. = any sub-package
    public void withinServicePackage() {}

    @Pointcut("within(dev.surya.orderapi.service.OrderService)")
    public void withinOrderService() {}

    // TYPE 4: target() — Match by the runtime type of the object
    // Matches when the object being called IS an instance of the specified type

    @Pointcut("target(dev.surya.orderapi.service.OrderService)")
    public void targetOrderService() {}
    // vs. within(): target() also matches subclasses at runtime
    // within() matches only the declared class (compile-time type)

    // TYPE 5: args() — Match by argument type at runtime
    // Useful when you want to intercept based on what data is being passed

    @Pointcut("args(dev.surya.orderapi.dto.PaymentDTO, ..)")
    public void methodsReceivingPayment() {}

    @Pointcut("args(Long)")
    public void methodsWithSingleLongArg() {}

    // ─── Combining Pointcuts with &&, ||, ! ──────────────────────────────────

    // All service methods EXCEPT getters (reads don't need transaction logging):
    @Pointcut("withinServicePackage() && !execution(* get*(..))")
    public void serviceNonGetters() {}

    // Performance logging: service methods OR annotated methods:
    @Pointcut("anyServiceMethod() || annotatedWithLogPerformance()")
    public void performanceTargets() {}

    // ─── Named Pointcut Reuse ────────────────────────────────────────────────

    @Before("anyServiceMethod()")
    public void logServiceEntry(JoinPoint jp) {
        log.info("→ Entering: {}.{}()",
            jp.getTarget().getClass().getSimpleName(),
            jp.getSignature().getName());
    }

    @AfterThrowing(pointcut = "anyServiceMethod()", throwing = "ex")
    public void logServiceException(JoinPoint jp, Exception ex) {
        log.error("✗ Exception in {}.{}(): {}",
            jp.getTarget().getClass().getSimpleName(),
            jp.getSignature().getName(),
            ex.getMessage());
    }

    @Around("annotatedWithLogPerformance()")
    public Object measureExecutionTime(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            Object result = pjp.proceed();
            log.info("✓ {}.{}() completed in {}ms",
                pjp.getTarget().getClass().getSimpleName(),
                pjp.getSignature().getName(),
                System.currentTimeMillis() - start);
            return result;
        } catch (Throwable t) {
            log.error("✗ {}.{}() failed after {}ms: {}",
                pjp.getTarget().getClass().getSimpleName(),
                pjp.getSignature().getName(),
                System.currentTimeMillis() - start,
                t.getMessage());
            throw t;
        }
    }
}

// ─── Custom Annotation ───────────────────────────────────────────────────────

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface LogPerformance {
    String value() default "";  // optional description
}

// ─── Usage Example ───────────────────────────────────────────────────────────

@Service
public class PaymentService {

    @LogPerformance("process-payment")
    @Transactional
    public PaymentResult processPayment(PaymentDTO dto) {
        // This method is intercepted by: annotatedWithLogPerformance() pointcut
        // AND by: anyServiceMethod() pointcut
        // Both aspects run (in order of @Order annotation if specified)
        return externalGateway.charge(dto);
    }
}
```

## 8.5 A complete performance logging aspect

```java
package com.example.ordermanagement.aspect;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;
import org.springframework.util.StopWatch;

@Aspect
@Component
@Slf4j
public class PerformanceLoggingAspect {

    /**
     * Named reusable pointcut — matches any public method in any class
     * in the service package or its sub-packages.
     */
    @Pointcut("execution(public * com.example.ordermanagement.service..*.*(..))")
    public void serviceLayerMethods() {}

    /**
     * Logs any service method that takes longer than 100ms.
     * A WARNING is also emitted for methods taking longer than 1 second.
     *
     * @param joinPoint represents the actual method call being intercepted
     */
    @Around("serviceLayerMethods()")
    public Object logSlowMethods(ProceedingJoinPoint joinPoint) throws Throwable {
        String className = joinPoint.getTarget().getClass().getSimpleName();
        String methodName = joinPoint.getSignature().getName();

        StopWatch watch = new StopWatch();
        watch.start();

        try {
            // This is where the real method executes.
            // The return value is what the caller will see.
            Object result = joinPoint.proceed();
            watch.stop();

            long elapsed = watch.getTotalTimeMillis();
            if (elapsed > 1000) {
                log.warn("SLOW: {}.{}() took {}ms — investigate for N+1 or missing index",
                        className, methodName, elapsed);
            } else if (elapsed > 100) {
                log.debug("Performance: {}.{}() completed in {}ms",
                        className, methodName, elapsed);
            }
            return result;

        } catch (Throwable e) {
            watch.stop();
            log.debug("Performance: {}.{}() threw {} after {}ms",
                    className, methodName, e.getClass().getSimpleName(),
                    watch.getTotalTimeMillis());
            throw e; // always rethrow — don't swallow exceptions in an AOP advice
        }
    }
}
```

This aspect applies to every public method in every service class — any order creation, product lookup, inventory check — without modifying any of those classes. Change the threshold from 100ms to 50ms, add structured logging, write the timing to a metrics counter — all in one place, in one class.

`@Component` is required in addition to `@Aspect` because `@Aspect` alone is an AspectJ annotation that Spring scans for but doesn't automatically register as a bean. Without `@Component`, the aspect class isn't a Spring bean at all and Spring's AOP infrastructure never sees it. With both annotations, component scanning finds it as a bean, and Spring's `AbstractAutoProxyCreator` finds it as an aspect to apply to other beans.

## 8.6 `@Around` + `proceed()`: the full interception lifecycle

`@Around` is the most powerful advice type because it controls the *entire* lifecycle of the method invocation, not just what happens before or after. The analogy to a servlet `Filter` (from Chapter 5) is exact:

```java
@Around("somePointcut()")
public Object advice(ProceedingJoinPoint pjp) throws Throwable {
    // BEFORE
    System.out.println("About to call " + pjp.getSignature().getName());

    Object result;
    try {
        result = pjp.proceed();    // THE REAL METHOD RUNS HERE
    } catch (Exception e) {
        // You can suppress the exception, rethrow it, or throw a different one
        throw e;
    }

    // AFTER RETURNING NORMALLY
    System.out.println("Method returned: " + result);
    return result;   // You can inspect or replace the return value
}
```

`pjp.proceed()` is what actually invokes the target method. If you never call it, the target never runs and you're returning whatever value you choose from the advice instead — this is exactly how Spring's `@Cacheable` AOP advice works: it checks the cache; if there's a hit, it returns the cached value without ever calling `pjp.proceed()`.

`pjp.proceed(Object[] args)` passes modified arguments to the target — you can validate, sanitize, or add to the arguments before the method sees them.

## 8.7 How `@Transactional` is implemented: complete picture

Now that the proxy mechanism is fully explained, the implementation of `@Transactional` can be described completely:

1. Spring's `TransactionInterceptor` is an AOP `@Around` advice, registered by `@EnableTransactionManagement` (which `@SpringBootApplication` activates automatically).

2. Its pointcut matches any method annotated with `@Transactional`, on any Spring-managed bean.

3. When `@Transactional` method `foo()` is invoked on the proxy, `TransactionInterceptor.invoke()` runs:
   - It inspects the `@Transactional` annotation's `propagation` attribute.
   - Based on propagation, it either joins an existing transaction (finds the existing connection bound to the `ThreadLocal`) or creates a new one (obtains a new connection from HikariCP, sets `autoCommit = false`, binds it to the `ThreadLocal`).
   - It calls `pjp.proceed()` — the real `foo()` runs. Any repository calls within `foo()` obtain their database connection from the same `ThreadLocal` — that's how they participate in the same transaction.
   - If `foo()` returns normally: the interceptor calls `connection.commit()` and releases the connection back to the pool.
   - If `foo()` throws a `RuntimeException` (or `Error`, or whatever `rollbackFor` specifies): the interceptor calls `connection.rollback()` and releases the connection.

This is everything `@Transactional` does. It is a proxy-based AOP `@Around` advice that wraps the method in JDBC transaction management — no more, no less. Understanding it this completely means you understand exactly why the self-invocation trap exists (the proxy is bypassed), exactly what `propagation = REQUIRES_NEW` does at the JDBC level (a second, independent `connection.setAutoCommit(false)` is obtained and committed independently), and exactly what `readOnly = true` does (the interceptor sets `connection.setReadOnly(true)` and instructs Hibernate to skip dirty-checking at flush time).

> **Interview Question — SDE-2:** "How does `@Transactional` know to roll back on a `RuntimeException` but not on a checked exception, and how would you change that behavior?"
>
> **Answer:** `TransactionInterceptor` catches the thrown `Throwable` and checks it against the `rollbackFor` and `noRollbackFor` settings on the `@Transactional` annotation. The default rule — roll back on unchecked exceptions (`RuntimeException` and `Error`), commit on checked exceptions — was a deliberate design choice made in the early 2000s: checked exceptions were considered "expected business conditions the caller should handle" (not failures) while unchecked exceptions were "programming errors or unrecoverable failures" that warrant rolling back. Whether that distinction was wise is debatable, but the mechanism is simply: if `exception instanceof RuntimeException || exception instanceof Error` matches the rollback rule, rollback; otherwise, commit. To override: `@Transactional(rollbackFor = Exception.class)` causes rollback on *any* exception, checked or not — this is the right setting for most service methods in a clean Spring Boot application, because letting a transaction commit after a checked exception that represented a failure is almost never the intent. `@Transactional(noRollbackFor = InsufficientStockException.class)` would let that specific exception not trigger a rollback even though it's a `RuntimeException`.

---

Chapter 9 addresses a question the entire book has deferred: if `ddl-auto: update` is not safe for production (and it isn't), how does the database schema actually get created and evolved safely? The answer is Flyway.
