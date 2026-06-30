---
type: linkedin-post
post_number: 27
scheduled_week: 14
scheduled_day: Tuesday
status: drafted
---
Why I'm specifically targeting fintech backend roles.

The engineering problems are different here.

At a content platform, a bug means users see the wrong post.
At a payment company, a bug means someone's money disappears or appears twice.

That difference changes how you design everything:

→ Idempotency is not optional — every payment endpoint must be safe to retry
→ Exactly-once semantics matter — Kafka transactions, not just at-least-once
→ Reconciliation is a feature — nightly job verifying every transaction matches settlement
→ Availability is measured in nines — 99.99% means 52 minutes of downtime per year

These constraints make fintech backend engineering harder than most,
but also cleaner. The rules are strict. The edge cases are well-defined.

The tech stack at Razorpay and PhonePe is exactly what I've been building:
Java, Spring Boot, Kafka, Redis, PostgreSQL, Kubernetes.

90 days in. The preparation was designed for this.

#Fintech #BackendEngineering #SDE2
