---
type: linkedin-post
post_number: 14
scheduled_week: 7
scheduled_day: Friday
status: drafted
---
How I protect the Order API from payment gateway failures.

[ATTACH: Circuit Breaker state diagram: CLOSED → OPEN → HALF_OPEN]

Without a circuit breaker:
Payment gateway goes down for 5 seconds.
100 threads pile up waiting for responses.
Connection pool exhausted. Order service goes down too.
One failure cascades into total outage.

With Resilience4j:

@CircuitBreaker(name = "paymentGateway", fallbackMethod = "payFallback")
public PaymentResult processPayment(PaymentRequest req) {
    return externalGateway.charge(req);
}

public PaymentResult payFallback(PaymentRequest req, Exception ex) {
    return PaymentResult.pendingRetry(req.getOrderId());
}

CLOSED → failing 50%+ over 10 calls → OPEN (instant fallback for 30s)
OPEN → probe with 1 real call → if success → CLOSED

The result: payment gateway outage = degraded service, not total failure.
Orders queue for retry. No cascading crash.

#SpringBoot #DistributedSystems #BackendEngineering
