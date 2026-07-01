---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 7 — Documentation & Production"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [spring, actuator, operations]
---

# Spring Boot Actuator

## Intuition
Actuator adds production-ready HTTP endpoints to your application that expose operational health and metrics. 
For example, `/actuator/health` returns `UP` if the application and its dependencies (database, disk space) are reachable.

## Custom Health Indicators
Spring auto-configures health checks for known resources (like the database). But if your application talks to a 3rd-party API, you should write a custom `HealthIndicator`:
```java
@Component("paymentGateway")
public class PaymentGatewayHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        // ping the gateway
        // if success: return Health.up().build();
        // if fail: return Health.down().withDetail("error", "timeout").build();
    }
}
```
If any component returns `DOWN`, the aggregate status becomes `DOWN`, which Kubernetes uses to determine if a pod should be restarted.
