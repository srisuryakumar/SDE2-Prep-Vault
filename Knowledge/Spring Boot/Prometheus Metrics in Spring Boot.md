---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 7 — Documentation & Production"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, metrics, operations]
---

# Prometheus Metrics in Spring Boot

## Intuition
With `micrometer-registry-prometheus` on the classpath, Actuator exposes an `/actuator/prometheus` endpoint containing JVM metrics, HTTP request latency, and HikariCP connection pool stats in Prometheus text format.

## Custom Metrics
You can use `MeterRegistry` to record custom business metrics (e.g. number of orders placed).
```java
@Service
public class MetricsService {
    private final Counter orderCreatedCounter;

    public MetricsService(MeterRegistry registry) {
        this.orderCreatedCounter = Counter.builder("orders.created")
                .description("Total number of orders created")
                .register(registry);
    }

    public void recordOrderCreated() {
        orderCreatedCounter.increment();
    }
}
```
You can then visualize these metrics using Grafana.
