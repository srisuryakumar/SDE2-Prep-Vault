---
type: linkedin-post
post_number: 26
scheduled_week: 13
scheduled_day: Friday
status: drafted
---
When a distributed transaction fails halfway, who cleans up?

Saga pattern — the answer.

Scenario: Order created → Payment charged → Inventory reserved.
Payment succeeds. Inventory reservation fails.

Without Saga: payment is charged, order is stuck. Money taken, item not coming.

With Saga — Choreography approach:

1. OrderService publishes: OrderCreated event
2. PaymentService listens → charges card → publishes: PaymentSucceeded
3. InventoryService listens → tries to reserve → publishes: InventoryFailed
4. PaymentService listens to InventoryFailed → runs compensating transaction: refund card

Each step has a compensating action that undoes it.
No 2-phase commit. No coordinator holding locks.

The code:
@KafkaListener(topics = "inventory.failed")
public void handleInventoryFailed(OrderEvent event) {
    paymentService.refund(event.getPaymentId());
    eventPublisher.publish(new PaymentRefunded(event.getOrderId()));
}

Implemented in scalable-ecommerce-platform: [GitHub link]

#DistributedSystems #Kafka #BackendEngineering
