---
type: linkedin-post
post_number: 11
scheduled_week: 6
scheduled_day: Tuesday
status: drafted
---
Kafka confused me for two weeks. Then I drew this and it clicked.

[ATTACH: Diagram of topic with 3 partitions and 2 consumer groups]

Key rules:
→ A partition is read by exactly ONE consumer per group at a time
→ More partitions = more parallelism within a group
→ Consumers > partitions = idle consumers (wasted)
→ Two consumer groups = independent reads of the same topic

Why partition by key?
If you process Order events, partition by order_id.
This guarantees all events for the same order arrive in sequence
at the same consumer. Order matters for stateful processing.

Why consumer lag is your most important Kafka metric:
Lag = latest offset − current offset per partition
Rising lag = your consumers can't keep up with producers
Alert when lag exceeds your SLA threshold.

#Kafka #DistributedSystems #BackendEngineering
