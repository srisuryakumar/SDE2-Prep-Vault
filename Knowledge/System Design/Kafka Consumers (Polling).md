---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Consumer Commit (Auto vs Manual)"]
tags: [kafka, messaging]
---

# Kafka Consumers (Polling)

## Intuition
Unlike some message queues that push messages to consumers, Kafka consumers **poll** (pull) messages from brokers.

## Why Pull over Push?
Pull-based consumption lets each consumer control its own pace. A slow consumer pulls messages only when it is ready. If a broker pushed messages at the broker's pace, a slow consumer would easily be overwhelmed and crash. 

```java
while (true) {
    // Consumer pulls a batch, completely controlling the pace
    records = consumer.poll(Duration.ofMillis(500));  
    for (record : records) {
        process(record);                              
    }
    consumer.commitSync();                             
}
```
