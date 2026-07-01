---
type: concept
title: In-Process Pub-Sub Event Bus LLD
tags: [lld, design, concurrency]
---
# In-Process Pub-Sub Event Bus LLD

## Requirements
- Decouple publishers from subscribers.
- Support multiple topics.
- Allow subscribers to listen to specific topics.
- Handle concurrent publishing and subscribing.

## Core Components
1. **EventBus**: The central dispatcher.
2. **Topic**: Represents a channel of communication.
3. **Event**: The message payload.
4. **Publisher**: Sends events to the bus.
5. **Subscriber**: Interface with an `onEvent(Event e)` method.

## Design Patterns Used
- **Mediator**: The EventBus acts as a mediator between Publishers and Subscribers.
- **Observer**: Subscribers observe the topics they care about.

## Concurrency Considerations
- The EventBus must use a thread-safe data structure to map Topics to a list of Subscribers, such as `ConcurrentHashMap<Topic, CopyOnWriteArrayList<Subscriber>>`.
- To prevent slow subscribers from blocking the publisher, events should ideally be dispatched asynchronously using a thread pool (`ExecutorService`).
