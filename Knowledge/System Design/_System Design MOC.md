---
type: moc
subject: System Design
status: to-study
---

# System Design MOC

Welcome to the System Design Map of Content. This MOC ties together concepts related to building scalable, reliable, and fault-tolerant distributed systems.

## 1. Fundamentals of Distributed Systems
- [[Why a single machine isn't enough]]
- [[The Eight Fallacies of Distributed Computing]]
- [[CAP Theorem]]
- [[CP vs AP Systems]]
- [[PACELC Theorem]]

## 2. Consistency Models
- [[Consistency Models Overview]]
- [[Strong Consistency (Linearizability)]]
- [[Sequential Consistency]]
- [[Causal Consistency]]
- [[Eventual Consistency]]
- **Client-Centric:**
  - [[Read-Your-Writes Consistency]]
  - [[Monotonic Reads]]
- [[Tunable Consistency (Cassandra)]]

## 3. Data Replication
- [[Database Replication (Why replicate)]]
- [[Leader-Follower (Master-Replica) Replication]]
- [[Multi-Leader Replication]]
- [[Leaderless Replication (Dynamo-style)]]

## 4. Partitioning & Sharding
- [[Partitioning (Sharding) Overview]]
- [[Hash Partitioning vs Range Partitioning]]
- [[Consistent Hashing]]
- [[Virtual Nodes (Consistent Hashing)]]
- [[Hot Spots in Distributed Systems]]

## 5. Message Brokers (Apache Kafka)
- [[Why Kafka Exists (Decoupling)]]
- [[Kafka Architecture Overview]]
- [[Kafka Producers (Partition Selection)]]
- [[Kafka Producer ACKs]]
- [[Idempotent Producers (Kafka)]]
- [[Kafka Consumers (Polling)]]
- [[Consumer Commit (Auto vs Manual)]]
- [[Consumer Group Rebalancing]]
- [[Consumer Lag]]
- [[Dead Letter Queue (DLQ) in Kafka]]
- [[Kafka Schema Registry]]
- [[Kafka Streams]]
- [[Kafka Exactly-Once Semantics (EOS)]]
- [[Kafka Topic Configuration (Partitions and Replication)]]
- [[Kafka Log Compaction vs Retention]]

## 6. Distributed Transactions & Idempotency
- [[Distributed Transactions Overview]]
- [[Two-Phase Commit (2PC)]]
- [[The Saga Pattern]]
- [[Saga Choreography vs Orchestration]]
- [[Idempotency in Distributed Systems]]

## 7. CQRS & Event Sourcing
- [[Event Sourcing]]
- [[CQRS (Command Query Responsibility Segregation)]]

## 8. Microservices Resilience & Infrastructure (Spring Cloud)
- [[Cascading Failures in Microservices]]
- [[API Gateway (Spring Cloud)]]
- [[Circuit Breaker Pattern]]
- [[Retry vs Circuit Breaker]]
- [[Spring Cloud Config and @RefreshScope]]
- [[Kubernetes Service Discovery vs Eureka]]

- [[BookMyShow (HLD)]]

- [[Distributed Job Scheduler (HLD)]]

- [[Feed Generation (HLD)]]

- [[Netflix (HLD)]]

- [[Notification System (HLD)]]

- [[Payment System (HLD)]]

- [[Rate Limiter (HLD)]]

- [[Search Autocomplete (HLD)]]

- [[System Design Building Blocks]]

- [[System Design Framework]]

- [[System Design Trade-offs]]

- [[URL Shortener (HLD)]]

- [[Uber (HLD)]]

- [[WhatsApp (HLD)]]


## Explicit Links
- [[System Design - Rate Limiter]]
