---
type: moc
subject: Spring Boot and Backend Engineering
---

# Spring Boot and Backend Engineering MOC

## HTTP & REST API Design
- [[Anatomy of an HTTP Request]]
- [[HTTP Methods (Safety and Idempotency)]]
- [[HTTP Status Codes]]
- [[HTTP Headers]]
- [[HTTP 1.1 vs HTTP 2]]
- [[HTTPS and TLS]]
- [[Resource Naming (Nouns, Not Verbs)]]
- [[API Versioning (URL vs Header)]]
- [[URL Design (Path vs Query Parameters)]]
- [[Consistent Response Shapes (Errors and Pagination)]]
- [[Offset vs Cursor Pagination)]]
- [[Idempotency Keys (Making POST Safe)]]
- [[Richardson Maturity Model (HATEOAS)]]

## Spring Boot Internals
- [[Spring Boot vs Spring Framework]]
- [[Dependency Injection (Constructor vs Field vs Setter)]]
- [[ApplicationContext vs BeanFactory]]
- [[Bean Scopes]]
- [[The Bean Lifecycle]]
- [[How Auto-Configuration Works]]
- [[@SpringBootApplication (The 3 Annotations)]]
- [[application.yml Precedence Hierarchy]]
- [[@Value vs @ConfigurationProperties]]
- [[ApplicationRunner and CommandLineRunner]]

## Spring Data JPA
- [[JPA Associations (OneToMany, ManyToOne, OneToOne)]]
- [[JPA Fetch Types (EAGER vs LAZY)]]
- [[@Version and Optimistic Locking (JPA)]]
- [[JpaRepository Hierarchy]]
- [[Spring Data JPA Derived Queries]]
- [[@Query (JPQL vs Native SQL)]]
- [[@Modifying and clearAutomatically]]
- [[Pagination (Page vs Slice)]]
- [[The N+1 Problem]]
- [[JOIN FETCH (Fixing N+1)]]
- [[@EntityGraph (Fixing N+1)]]
- [[@BatchSize (Fixing N+1)]]

## Spring MVC & Service Layer
- [[@Transactional (What it actually does)]]
- [[Transaction Propagation]]
- [[The Self-Invocation Trap (Spring AOP)]]
- [[@Transactional(readOnly = true)]]
- [[DTOs vs Entities]]
- [[@RestController vs @Controller]]
- [[Request Mapping Annotations]]
- [[ResponseEntity (Controlling HTTP Responses)]]
- [[Bean Validation (@Valid and Constraints)]]
- [[Custom Constraint Annotations]]
- [[@RestControllerAdvice (Global Exception Handler)]]

## Security JWT
- [[Stateless Authentication]]
- [[JWT Structure]]
- [[Spring Security Core Filter Chain]]
- [[JwtAuthenticationFilter (Spring Security)]]
- [[Method-Level Security (@PreAuthorize)]]
- [[CORS vs CSRF]]

## Testing
- [[The Testing Pyramid]]
- [[@MockitoBean vs @MockBean]]
- [[@WebMvcTest (Controller Layer Tests)]]
- [[@DataJpaTest (Repository Layer Tests)]]
- [[@SpringBootTest (Integration Tests)]]
- [[Testcontainers vs H2]]

## Documentation & Production
- [[OpenAPI and springdoc]]
- [[Spring Boot Actuator]]
- [[Prometheus Metrics in Spring Boot]]
- [[Spring Profiles]]
- [[Graceful Shutdown]]

## Spring AOP
- [[Cross-Cutting Concerns]]
- [[Spring AOP Proxy Model]]
- [[AOP Vocabulary]]
- [[Pointcut Expressions]]
- [[@Around and proceed()]]
- [[How @Transactional is implemented]]

## Flyway & Database Migrations
- [[The Problem with ddl-auto update]]
- [[Flyway Core Concepts]]
- [[Zero-Downtime Database Migrations]]
- [[Adding Columns Safely]]
- [[Concurrent Index Creation (PostgreSQL)]]

## Deployment
- [[Multi-Stage Docker Builds (Spring Boot)]]
- [[JVM Memory Limits in Containers]]
- [[The Value of a Live Swagger UI]]
