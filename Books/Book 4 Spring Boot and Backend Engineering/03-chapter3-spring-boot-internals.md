# Chapter 3: Spring Boot Internals

This is the chapter that turns "I can follow a tutorial" into "I can explain what's actually happening." Everything from here on is Spring Boot code, and every later chapter leans on the mental model built here — when Chapter 4 says "the proxy intercepts the call," this is where you learn what a proxy is and why one exists in the first place.

## 3.1 What Spring Boot actually is

Spring Framework, on its own, is a dependency-injection container and a collection of modules (web MVC, data access, security, and so on) — powerful, but historically notorious for requiring pages of XML or Java configuration before a single request could be handled. Spring Boot doesn't replace Spring Framework; it sits on top of it and does two specific things:

**Convention over configuration.** Spring Boot ships with opinionated defaults for almost everything. If you add a JPA starter and a PostgreSQL driver to your classpath, Spring Boot assumes you want a `DataSource` pointed at PostgreSQL, a `JpaTransactionManager`, and Hibernate as the JPA provider — and configures all three for you, with sensible defaults, without you writing a single bean definition. You only write configuration when you want to *override* a default, not to establish a baseline.

**Auto-configuration.** This is the mechanism that makes the above possible, and it's worth understanding precisely because "it's magic" is not an acceptable answer in an interview — Section 3.3 walks through exactly how it decides what to configure.

The payoff is the thing every Spring Boot tutorial shows off: a `main()` method, one annotation, and a working embedded web server. The rest of this chapter is about not stopping at "it works" and instead being able to say *why*.

## 3.2 Setting up the project

We'll use Maven, Java 21, and Spring Boot 3.5.x for the reasons explained in the README. Generate a project from [start.spring.io](https://start.spring.io) with the Web, Validation, and Lombok dependencies to start (we add JPA, Security, and the rest as each chapter needs them), or create this `pom.xml` directly:

**`pom.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.5.13</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>order-management</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>order-management</name>
    <description>Order Management API — companion project for Spring Boot and Backend Engineering</description>

    <properties>
        <java.version>21</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

`spring-boot-starter-parent` is what lets every other dependency in this file omit a `<version>` — it's a parent POM that pins compatible versions of everything in the wider Spring Boot ecosystem (Jackson, Hibernate, Tomcat, and dozens more) to versions known to work together. This is itself a small example of convention over configuration: figuring out which Jackson version is compatible with which Hibernate version is exactly the kind of bookkeeping Spring Boot exists to take off your plate.

A quick, honest note on Lombok, since we'll lean on it for entities and DTOs starting in Chapter 4: `@Getter`, `@Setter`, `@RequiredArgsConstructor`, and friends are **not** runtime magic — Lombok is an annotation processor that runs at *compile time* and literally generates the boilerplate Java source (getters, setters, constructors) into your `.class` files before `javac` finishes. If you decompiled the compiled class, you'd see ordinary, hand-written-looking getter and setter methods — Lombok just saved you from typing them. It's worth being able to say this in an interview, because "Lombok adds methods via reflection at runtime" is a common and incorrect answer.

## 3.3 `@SpringBootApplication`: one annotation, three jobs

```java
package com.example.ordermanagement;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class OrderManagementApplication {

    public static void main(String[] args) {
        SpringApplication.run(OrderManagementApplication.class, args);
    }
}
```

`@SpringBootApplication` is a meta-annotation — an annotation that's just a bundle of other annotations, applied as a convenience. Unwrapped, it's:

```java
@SpringBootConfiguration   // itself meta-annotated with @Configuration
@EnableAutoConfiguration
@ComponentScan
public @interface SpringBootApplication { ... }
```

Each piece has a distinct job:

**`@Configuration`** (via `@SpringBootConfiguration`) marks this class as a source of bean definitions — the same annotation you'd put on any class containing `@Bean`-annotated factory methods. The main class doesn't have to define any `@Bean` methods itself, but it's eligible to.

**`@EnableAutoConfiguration`** is the trigger for the entire auto-configuration mechanism described in the next section — it tells Spring Boot "go inspect the classpath and conditionally activate whatever configuration classes make sense given what's actually present."

**`@ComponentScan`** tells Spring to scan for `@Component`-annotated classes (and its specializations — `@Service`, `@Repository`, `@Controller`) starting from the package the annotated class lives in, and recursively through every sub-package. This is *why* the convention is to put your main class in the root package (`com.example.ordermanagement`, with everything else nested under it) — a class in a sibling package, or worse, a parent package, simply won't be found, because component scanning by default only looks downward from where it starts.

> **Interview Question — SDE-2:** "If you moved your main application class into a sub-package like `com.example.ordermanagement.app`, what would break?"
>
> **Answer:** Component scanning is rooted at the package of the `@SpringBootApplication`-annotated class and only scans downward from there. Moving the main class into a sub-package means anything in `com.example.ordermanagement.entity`, `.repository`, `.service`, and so on — all the actual application code — now lives *outside* the scan path, since those packages are siblings of `app`, not descendants of it. None of those beans get registered, and the application fails at startup the moment something tries to inject one of them (a missing-bean `NoSuchBeanDefinitionException`), or simply silently has no controllers mapped at all. The fix is either moving the main class back to the root package, or explicitly widening the scan with `@ComponentScan(basePackages = "com.example.ordermanagement")`.

## 3.4 How auto-configuration actually decides what to configure

This is the part most tutorials wave away as "magic." It isn't — it's a layered system of conditional checks, and you can read the actual source if you want to (it's all open source, in `spring-boot-autoconfigure`).

**Step 1 — discovery.** When the application starts, Spring Boot needs a list of *candidate* auto-configuration classes to consider. In Spring Boot 2.7 and later (which includes every 3.x version this book targets), that list comes from a plain-text file: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, packaged inside each starter JAR, listing one fully-qualified configuration class name per line. (If you read older material — and a lot of it is still out there — you'll see this described as living in `META-INF/spring.factories` under the key `org.springframework.boot.autoconfigure.EnableAutoConfiguration`. That file format is the *pre-2.7* mechanism; `spring.factories` still exists and is still used for a handful of other Spring Boot extension points, but autoconfiguration discovery specifically moved to the dedicated `.imports` file. Knowing both names is worth it precisely because so much existing documentation and so many Stack Overflow answers still reference the older one.)

**Step 2 — conditional evaluation.** Spring Boot doesn't activate every candidate it found — most of them guard themselves with condition annotations, and only the ones whose conditions are satisfied actually contribute beans. The two you'll see constantly:

```java
@Configuration
@ConditionalOnClass(DataSource.class)
public class DataSourceAutoConfiguration {
    // only even considered if a DataSource class is on the classpath at all —
    // i.e., you've added a JDBC driver dependency
}
```

```java
@Bean
@ConditionalOnMissingBean(PasswordEncoder.class)
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

`@ConditionalOnClass` checks the classpath — does a given class exist at all, meaning some dependency that provides it was added. `@ConditionalOnMissingBean` checks the `ApplicationContext` that's been built *so far* — has anything (auto-configuration or your own code) already registered a bean of this type? This second one is exactly why auto-configuration is "configure unless overridden," not "configure no matter what": if you define your own `PasswordEncoder` bean anywhere in your own `@Configuration` classes, Spring Boot's auto-configured default backs off entirely, because by the time it's evaluated, the condition is no longer true. There's a longer family of these — `@ConditionalOnProperty` (a specific `application.yml` value must be set, optionally to a specific value), `@ConditionalOnWebApplication`, `@ConditionalOnBean` — all following the same pattern: a declarative gate that decides whether a chunk of configuration applies to *this* application, given everything that's true about it.

Concretely, this is why adding `spring-boot-starter-data-jpa` plus a PostgreSQL driver to your `pom.xml` and writing a connection URL in `application.yml` is enough to get a fully working `DataSource`, `EntityManagerFactory`, and `JpaTransactionManager`, with zero `@Bean` methods of your own: `DataSourceAutoConfiguration`'s `@ConditionalOnClass(DataSource.class)` is satisfied (the JDBC driver put it on the classpath), there's no competing `DataSource` bean of your own, so it activates and wires one up using the properties you supplied.

> **Interview Question — SDE-2:** "How does Spring Boot decide whether to auto-configure a `DataSource`, and how would you prevent it from doing so?"
>
> **Answer:** It's gated by `@ConditionalOnClass` on the JDBC driver/`DataSource` API being present on the classpath, and `@ConditionalOnMissingBean` ensuring no `DataSource` bean already exists. To prevent it, you have a few real options: don't put a JDBC driver on the classpath at all; define your own `DataSource` `@Bean` (the missing-bean condition then fails and Boot's default backs off); or explicitly exclude the auto-configuration class via `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)` or the equivalent `spring.autoconfigure.exclude` property, which is the most explicit and most common approach when you genuinely don't want a feature that Boot would otherwise enable based on what's on your classpath.

## 3.5 The IoC container and the bean lifecycle

"IoC" (Inversion of Control) just means: instead of your code calling `new` and wiring up its own dependencies, you describe what you need, and a container builds and hands you fully-wired objects. That container, inside Spring, is the `ApplicationContext`, and the objects it manages are **beans**.

A bean's life, from the container's point of view, runs through a fixed sequence:

1. **Instantiation** — the container calls the bean's constructor.
2. **Dependency injection** — if the bean has dependencies (via constructor parameters, `@Autowired` setters, or `@Autowired` fields), the container supplies them. For constructor injection, steps 1 and 2 actually happen together — you cannot construct the object without its constructor arguments, so the container must have already resolved and built any beans this one depends on.
3. **`Aware` callbacks** — if a bean implements marker interfaces like `BeanNameAware` or `ApplicationContextAware`, the container calls those setters now, handing the bean a reference to its own name or to the context itself. Rare in application code; common in framework and library code.
4. **`BeanPostProcessor#postProcessBeforeInitialization`** — a hook that runs on *every* bean, used internally by Spring (and by libraries like Lombok-adjacent tooling, validation frameworks, and AOP) to inspect or wrap beans before initialization callbacks run. This is also, not coincidentally, the mechanism the AOP proxy machinery from Chapter 8 hooks into.
5. **`@PostConstruct`** (or `InitializingBean#afterPropertiesSet()`) — your bean's own initialization logic, guaranteed to run *after* dependency injection is complete. This is the right place for "now that all my dependencies are set, do some setup" — opening a connection, validating configuration, warming a cache.
6. **`BeanPostProcessor#postProcessAfterInitialization`** — another universal hook, run after your `@PostConstruct`. This is specifically where Spring AOP proxies get created — if a bean needs to be wrapped in a proxy (because it has `@Transactional` methods, for example), the *real* object you constructed becomes the proxy's internal target here, and the reference everyone else in the container actually receives is the proxy, not your original instance. Chapter 8 covers exactly what that proxy does and why it matters.
7. **Ready for use** — the bean now sits in the container, available for injection into other beans, for the lifetime of the application context.
8. **`@PreDestroy`** (or `DisposableBean#destroy()`) — called when the context shuts down, in reverse order of creation, giving each bean a chance to release resources: closing connections, flushing buffers, stopping background threads.

You can watch this sequence happen, in order, with three tiny classes:

**`com/example/ordermanagement/demo/StartupBanner.java`**
```java
package com.example.ordermanagement.demo;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class StartupBanner {

    private static final Logger log = LoggerFactory.getLogger(StartupBanner.class);

    public StartupBanner() {
        log.info("[1] Constructor — instance exists; @PostConstruct has not run yet.");
    }

    @PostConstruct
    public void init() {
        log.info("[3] @PostConstruct — dependency injection finished; this bean is fully wired.");
    }

    @PreDestroy
    public void cleanup() {
        log.info("[*] @PreDestroy — context is shutting down, releasing resources now.");
    }
}
```

**`com/example/ordermanagement/demo/StartupRunner.java`**
```java
package com.example.ordermanagement.demo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupRunner implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(StartupRunner.class);
    private final StartupBanner startupBanner;

    public StartupRunner(StartupBanner startupBanner) {
        this.startupBanner = startupBanner;
        log.info("[2] StartupRunner constructed — Spring had to fully build StartupBanner first to hand it to me here.");
    }

    @Override
    public void run(ApplicationArguments args) {
        log.info("[4] ApplicationRunner#run — the whole context is refreshed; every singleton exists and is initialized. " +
                "This runs immediately before Boot logs 'Started OrderManagementApplication'.");
    }
}
```

Run the application and the log output appears in exactly that numbered order — `[1]`, `[2]`, `[3]` (for `StartupBanner` — note its `@PostConstruct` actually fires *before* the constructor log of `StartupRunner` would suggest, because Spring fully completes one bean, including its `@PostConstruct`, before moving on to construct the next one that depends on it), then `[4]`, then Boot's own "Started" line. Seeing it rather than just reading about it is worth the four files — it turns "the bean lifecycle" from an abstract list into something you've watched happen.

> **Interview Question — SDE-2:** "What's the practical difference between doing setup work in a constructor versus in `@PostConstruct`?"
>
> **Answer:** A constructor can only safely use what's passed as its own parameters — at the point the constructor body runs, *this* bean's fields are being set, but there's no guarantee about the broader wiring of the application context beyond this bean's own direct dependencies. `@PostConstruct` runs strictly after the container has finished injecting everything this bean declared as a dependency, so it's the safe place to call methods *on* those dependencies as part of setup — e.g., calling a method on an injected service to prime a cache. It also separates "build the object" from "the object is ready to do work," which matters if a subclass or a testing framework wants to construct the object without immediately triggering side effects.

## 3.6 How Spring discovers beans: `@Component` and its specializations

`@ComponentScan` looks for one annotation: `@Component`. The four annotations you'll write constantly — `@Component`, `@Service`, `@Repository`, `@Controller` — are not four independent mechanisms; three of them are meta-annotated with `@Component` itself:

```java
@Component
public @interface Service { ... }

@Component
public @interface Repository { ... }

@Component
public @interface Controller { ... }
```

Which means component scanning finds beans annotated with any of the four identically — as far as *discovery* goes, `@Service` and `@Component` are interchangeable. The specializations exist for two other reasons: **semantic clarity** (a glance at `@Service` on a class tells you it's business logic, `@Repository` tells you it's a data-access class, `@Controller` tells you it handles HTTP, without reading the class body), and, for `@Repository` specifically, **one piece of real extra behavior**: it's the trigger for Spring's `PersistenceExceptionTranslationPostProcessor`, which catches the native, technology-specific exceptions Hibernate/JDBC throw and translates them into Spring's own consistent `DataAccessException` hierarchy. That's exactly why, when we look at optimistic locking failures in Chapter 4, the exception you actually catch in a `@RestControllerAdvice` is a Spring exception (`ObjectOptimisticLockingFailureException`), not Hibernate's native one (`StaleObjectStateException`) — `@Repository` is what makes that translation happen automatically.

> **Interview Question — SDE-2:** "Could you swap every `@Service` and `@Repository` in a codebase for plain `@Component` and have it still work?"
>
> **Answer:** Discovery-wise, yes — component scanning treats them identically, since both are meta-annotated with `@Component`. But it's not free: `@Repository`'s exception-translation behavior (turning Hibernate/JDBC-native exceptions into Spring's `DataAccessException` hierarchy) is tied specifically to that annotation, so a data-access class annotated `@Component` instead of `@Repository` would leak the underlying persistence provider's native exceptions to its callers instead of Spring's consistent abstraction — a real behavioral regression, not just a style loss. `@Service` and `@Controller` carry no equivalent hidden behavior, so swapping those specifically is purely cosmetic, but doing it across the board would still be bad practice: the semantic signal of "what kind of class is this" is genuinely useful to the next engineer reading the code.

## 3.7 Dependency injection: constructor, setter, and field

Spring supports injecting dependencies three ways. All three exist; only one is the right default.

```java
// Field injection — works, but avoid it as a default
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
}

// Setter injection — used for optional dependencies
@Service
public class OrderService {
    private NotificationService notificationService;

    @Autowired
    public void setNotificationService(NotificationService notificationService) {
        this.notificationService = notificationService;
    }
}

// Constructor injection — the default this book uses everywhere
@Service
public class OrderService {
    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }
}
```

With Lombok, that last form is just:

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
}
```

`@RequiredArgsConstructor` generates exactly the constructor written out above, for every `final` field — it's compile-time codegen, not a different injection mechanism, which is why it's still constructor injection underneath.

Why constructor injection is the recommended default, concretely:

**Immutability.** A constructor-injected dependency can be `final`. It's set exactly once, at construction, and can never be reassigned — which rules out an entire category of bugs where some code path accidentally mutates a dependency reference mid-lifecycle.

**Fail fast, and fail at the right layer.** If `OrderRepository` can't be resolved — missing bean, circular dependency, whatever — a constructor-injected class fails to even *construct*, at application startup, with a clear stack trace pointing at the constructor. A field-injected class will construct fine (the no-arg constructor doesn't need the field) and only blow up with a `NullPointerException` the first time something tries to *use* the unset field, possibly in production, possibly on a rarely-hit code path, long after startup looked successful.

**Testability without a container.** `new OrderService(mockRepository)` is a plain Java constructor call — you can unit test `OrderService` with Mockito mocks and zero Spring involvement, which is exactly what Chapter 6's unit tests do. Field injection has no public setter and no constructor parameter for the dependency, so testing it without Spring's reflection-based test support means resorting to reflection hacks to set a private field — workable, but a clear sign the design is fighting you.

**Circular dependencies surface immediately, instead of being silently tolerated.** If `A` constructor-injects `B` and `B` constructor-injects `A`, Spring cannot resolve either — there's no valid order to construct them in — and it fails at startup with a clear `BeanCurrentlyInCreationException`. Field injection can sometimes paper over the same circular design by deferring resolution, which doesn't fix the underlying problem — a circular dependency between two services is almost always a sign of a service boundary actually drawn in the wrong place — it just delays when you find out.

> **Interview Question — SDE-2:** "If constructor injection is strictly better, why does field injection still exist and why do people still use it?"
>
> **Answer:** It exists because it's the most concise to type and was, historically, what most tutorials demonstrated first. People still reach for it in throwaway code, demos, or test classes where the downsides — mutability, hidden failure modes, harder testing — matter less because the code's lifespan is short. In production codebases, though, it's broadly considered a smell, to the point that static analysis tools (Spring's own `@Autowired` Javadoc, IDE inspections in IntelliJ) actively flag field injection with a warning recommending constructor injection instead. The honest answer to "why does it persist" is inertia and brevity, not that it has some advantage constructor injection lacks.

## 3.8 Bean scopes

By default, every bean in a Spring container is a **singleton** — exactly one instance, created once, shared by every part of the application that injects it. That's almost always what you want for stateless services, repositories, and controllers. Three other scopes exist for genuinely different needs:

| Scope | Lifetime | Typical use |
|---|---|---|
| `singleton` (default) | One instance for the entire application context | Services, repositories, controllers — anything stateless |
| `prototype` | A brand-new instance every time the bean is requested/injected | A bean that holds mutable, request-specific state and genuinely can't be shared — uncommon in typical REST APIs |
| `request` | One instance per HTTP request, shared across that request, then discarded | Holding data scoped to a single request that multiple components within it need to share |
| `session` | One instance per HTTP session | Holding data across multiple requests from the same client session — rare in a stateless, JWT-based API like ours |

A genuine subtlety worth knowing: injecting a narrower-scoped bean (`request` or `session`) into a `singleton` bean is a real problem, because the singleton is constructed once, long before any HTTP request exists, so there's no actual request to scope to at that point. Spring solves this with **scoped proxies** — instead of injecting the real `request`-scoped object, the singleton receives a proxy that, on every method call, looks up "the real instance for the *currently active* request" and delegates to it. This is configured with `@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)`. This book's API is intentionally stateless (that's the entire premise of the JWT-based security in Chapter 5), so we don't reach for `request` or `session` scope anywhere in the actual project — but understanding why the proxy trick exists is exactly the kind of thing that comes up when an interviewer wants to know you understand scopes beyond their names.

> **Interview Question — SDE-2:** "What happens if you inject a `prototype`-scoped bean directly into a `singleton` bean's constructor?"
>
> **Answer:** You get exactly one instance of the prototype bean, created once, at the moment the singleton is constructed — and then that single instance is held by the singleton for its entire lifetime. This defeats the entire purpose of prototype scope, which is "a fresh instance every time it's needed." The injection only happens once, at construction time, so "every time it's needed" collapses to "the one time the singleton itself was built." If you genuinely need a fresh prototype instance on every *use*, not just on the singleton's own construction, you need either a scoped proxy (same mechanism as request/session scope) or to inject an `ObjectFactory<T>`/`ObjectProvider<T>` and call `.getObject()` each time you actually need a new instance, deferring the lookup instead of resolving it once at injection time.

## 3.9 `ApplicationContext` vs. `BeanFactory`

`BeanFactory` is the root interface — the most basic possible DI container: it can hold bean definitions and produce beans on request, lazily, one at a time. `ApplicationContext` extends `BeanFactory` and adds the features that make Spring an actual application framework rather than just a DI container: an event-publishing mechanism (`ApplicationEventPublisher` — beans can publish and listen for application events), internationalization support (`MessageSource`), the `Environment` abstraction that's how profiles and property sources work (Section 3.10), integration with AOP, and — critically — **eager initialization of singletons by default**, meaning every singleton bean is constructed at startup, not lazily on first use, so configuration mistakes surface immediately at boot rather than on whatever unlucky request happens to trigger them first.

In practice, you will essentially never interact with `BeanFactory` directly in application code — `ApplicationContext` (specifically `AnnotationConfigServletWebServerApplicationContext` for a typical Spring Boot web app) is what `SpringApplication.run()` creates and what backs the entire application. The distinction matters for interviews more than for day-to-day coding: it demonstrates you understand that Spring's DI container is layered, with `BeanFactory` as the minimal core and `ApplicationContext` as the production-grade superset.

> **Interview Question — SDE-2:** "Why does `ApplicationContext` eagerly initialize singletons by default, and is that ever a problem?"
>
> **Answer:** It's a deliberate fail-fast design: if a bean's configuration is broken — a missing required property, an unsatisfiable dependency, a bug in a `@PostConstruct` method — you want the application to refuse to start, loudly, with a clear stack trace, rather than start up looking healthy and then fail the first time a request happens to touch the broken bean, possibly hours after deployment, in production. The trade-off is startup time: an application with hundreds of singleton beans pays the full construction cost of all of them upfront, even ones that might never actually be used in a given run. For most applications this is a good trade. Where it isn't — very large applications, or specific beans that are genuinely expensive to construct and rarely used — `@Lazy` lets you opt a specific bean out of eager initialization on a case-by-case basis, deferring its construction to first use, without losing eager initialization everywhere else.

## 3.10 The startup sequence: from `main()` to "Started"

When `SpringApplication.run(OrderManagementApplication.class, args)` executes, roughly this happens, in order:

1. **The `Environment` is prepared.** Before a single bean is created, Spring Boot assembles a layered view of all configuration: command-line arguments, JVM system properties, OS environment variables, and every `application*.yml`/`.properties` file it can find — all merged into one `Environment` object, with a strict precedence order (Section 3.10 below covers this in full). This has to happen first because later steps — like deciding which profile is active — depend on it.
2. **An `ApplicationContext` is created**, of the appropriate type for the detected environment (a servlet-based web context, given `spring-boot-starter-web` is on the classpath).
3. **Bean definitions are loaded** — both from your own `@Component`-family classes (via component scanning) and from whatever auto-configuration classes passed their conditional checks (Section 3.3).
4. **The context is "refreshed."** This is the actual moment of construction: every singleton bean is instantiated, wired, and run through the full lifecycle from Section 3.5, in dependency order (if `A` needs `B`, `B` is fully built first).
5. **`ApplicationRunner` and `CommandLineRunner` beans execute**, in that order if both exist, after the context is fully refreshed but before the embedded server is reported as ready — this is exactly the hook our `StartupRunner` demo used.
6. **The embedded Tomcat server starts listening** on the configured port.
7. Boot logs the line everyone recognizes: `Started OrderManagementApplication in 1.847 seconds (process running for 2.103)` — that duration is measured from the very start of `main()`, which is *why* it's a genuinely useful number for tracking regressions in your own startup time as the application grows (a few hundred extra milliseconds creeping in over months of adding dependencies is a real, trackable cost).

> **Interview Question — SDE-2:** "If you wanted code to run once, exactly at startup, after the application is fully wired but before it starts accepting HTTP traffic — where would you put it, and why not just a `static` block or a `@PostConstruct`?"
>
> **Answer:** `ApplicationRunner` (or `CommandLineRunner`, if you specifically want raw `String[] args` rather than Spring Boot's parsed `ApplicationArguments`). A `static` initializer runs at class-loading time, with no guarantee the Spring context — or any bean you'd want to use — exists yet at all; it's outside the container's lifecycle entirely. `@PostConstruct` runs *per-bean*, as soon as that individual bean's own dependencies are wired — useful for that bean's own setup, but it doesn't guarantee the *entire* application context, every other bean, is fully constructed yet, since beans initialize in dependency order, not in some "everything, then go" order. `ApplicationRunner#run()` specifically executes after the whole context has finished refreshing — every singleton exists and is initialized — which is the right and only correctly-ordered hook for "run this once, when the whole application is genuinely ready, but before serving traffic."

## 3.11 The `application.yml` hierarchy

Spring Boot doesn't read configuration from one place — it merges many sources into a single `Environment`, with a strict precedence order when the same property is defined in more than one place. The full official order has more rungs than you need to memorize, but the ones that matter for day-to-day work, from highest precedence (wins) to lowest:

1. **Command-line arguments** (`--server.port=9090`) — highest precedence; useful for one-off overrides without touching any file.
2. **OS environment variables** (`SERVER_PORT=9090`) — this is how production secrets and per-environment values get in without ever being committed to source control; Spring Boot automatically "relaxes" the binding so `SERVER_PORT` maps to `server.port` and `SPRING_DATASOURCE_PASSWORD` maps to `spring.datasource.password`.
3. **Profile-specific files** (`application-prod.yml`, when the `prod` profile is active) — covered fully in Chapter 7, where we introduce `application-local.yml` and `application-prod.yml` alongside `SPRING_PROFILES_ACTIVE`.
4. **The base `application.yml`** — defaults that apply regardless of profile, unless a higher-precedence source overrides them.

The practical rule that falls out of this: put safe, non-secret defaults in `application.yml`; put per-environment differences (which database, which log level) in profile-specific files; and put actual secrets (database passwords, JWT signing keys, API keys for third parties) in environment variables, never committed to a file at all — both because environment variables sit higher in precedence (easy to override per-deployment without touching code) and, far more importantly, because a secret typed into a YAML file is a secret that's one `git add .` away from being in your commit history forever.

Here's the file as it stands after this chapter — small, but it'll grow every chapter from here:

**`src/main/resources/application.yml`**
```yaml
server:
  port: 8080

spring:
  application:
    name: order-management

ordermanagement:
  name: "Order Management API"
  support-email: "support@ordermanagement.com"
  max-items-per-order: 50

logging:
  level:
    com.example.ordermanagement: DEBUG
```

## 3.12 `@Value` vs. `@ConfigurationProperties`

Both pull values out of the merged `Environment` from Section 3.11 into your code; they exist for different shapes of problem.

**`@Value`** injects a single property into a single field, with optional Spring Expression Language (SpEL) and a default value syntax:

```java
@Value("${ordermanagement.name}")
private String appName;

@Value("${ordermanagement.max-items-per-order:25}")
private int maxItemsPerOrder;   // 25 is the default if the property is absent
```

This is fine for one or two scattered values, but it has real downsides at scale: there's no compile-time check that `ordermanagement.max-items-per-order` is spelled correctly anywhere — a typo just silently injects the default (or, with no default, throws at startup with a message that takes a moment to trace back to the typo) — and there's no single place that documents "here are all the configuration values this application understands."

**`@ConfigurationProperties`** binds an entire *group* of related properties into one typed, structured object, in one place:

```java
package com.example.ordermanagement.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "ordermanagement")
public record OrderManagementProperties(
        String name,
        String supportEmail,
        int maxItemsPerOrder
) {
}
```

With `@ConfigurationPropertiesScan` already on the main application class (Section 3.3), this record is automatically discovered and registered as a bean — no `@EnableConfigurationProperties(OrderManagementProperties.class)` needed, though that's the explicit alternative if you'd rather opt in class-by-class. Notice the field names use camelCase (`supportEmail`, `maxItemsPerOrder`) while the YAML uses kebab-case (`support-email`, `max-items-per-order`) — Spring Boot's **relaxed binding** automatically reconciles `kebab-case`, `camelCase`, and even `SCREAMING_SNAKE_CASE` (the form environment variables are forced into) as the same logical property, so whichever convention is natural for the source you're writing in just works.

Any other bean can now ask for this typed configuration directly:

```java
@Service
@RequiredArgsConstructor
public class SupportInfoService {
    private final OrderManagementProperties properties;

    public String getSupportEmail() {
        return properties.supportEmail();
    }
}
```

The practical guidance: reach for `@Value` for a genuinely isolated, one-off property; reach for `@ConfigurationProperties` the moment you have more than two or three related settings, because it gives you compile-time-checked, IDE-autocompletable, centrally documented configuration instead of a scatter of string-keyed lookups. We use it again for JWT settings in Chapter 5.

> **Interview Question — SDE-2:** "What's the actual mechanical difference between `@Value` and `@ConfigurationProperties` — not just 'one is for groups' — in how Spring resolves them?"
>
> **Answer:** `@Value` is resolved through SpEL at the point of injection, against the live `Environment` — it's a direct, one-shot string lookup (with an optional default) wherever the annotation is written. `@ConfigurationProperties` is a structured binding process: Spring Boot's `Binder` API walks the target class's properties (via its constructor for immutable types like this record, or via setters for a mutable POJO), and for each one, looks up the corresponding relaxed-form key in the `Environment` and converts it to the target type, including nested objects, lists, and maps — `@Value` has no equivalent for binding nested structures; it's fundamentally a single-key, single-value mechanism, while `@ConfigurationProperties` is a whole-object binder.

---

The project now boots, wires beans, and reads configuration — but it doesn't do anything yet. Chapter 4 is where the Order Management API itself actually gets built, starting with the data it needs to persist.
