---
type: linkedin-post
post_number: 10
scheduled_week: 5
scheduled_day: Friday
status: drafted
---
How @Transactional actually works — and the trap that breaks it silently.

Most developers think:
@Transactional = database transaction. Done.

What actually happens:
Spring creates a PROXY around your @Service class.
The proxy intercepts method calls, opens a transaction,
calls your method, then commits or rolls back.

The hidden trap — self-invocation:

@Service
public class OrderService {
    @Transactional
    public void processOrder(Long id) {
        updateStatus(id);
        sendNotification(id); // ← @Transactional IGNORED
    }

    @Transactional(propagation = REQUIRES_NEW)
    public void sendNotification(Long id) {
        // This does NOT run in a new transaction!
        // Called directly on 'this', not through the proxy.
    }
}

Fix: move sendNotification() to a separate @Service.

This is the most common Spring interview question and the most
common production bug I've seen in Spring Boot codebases.

#SpringBoot #Java #BackendEngineering
