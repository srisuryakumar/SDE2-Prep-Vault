---
type: concept
title: Generic Cache System Design LLD
tags: [lld, design, caching]
---
# Generic Cache System Design LLD

## Requirements
- Key-Value storage with generics `<K, V>`.
- Configurable eviction policies (LRU, LFU, FIFO).
- Configurable time-to-live (TTL) expiration.
- Thread-safe for concurrent reads and writes.

## Core Components
1. **Cache<K, V>**: Interface defining `put`, `get`, `remove`, `clear`.
2. **CacheEntry<V>**: Wrapper containing the value, creation time, last access time, and access frequency.
3. **EvictionStrategy<K, V>**: Interface for eviction logic (`evict()`).
4. **Storage**: The underlying data structure, usually a `ConcurrentHashMap`.

## Eviction Implementations
- **LRU (Least Recently Used)**: Implemented using a Doubly Linked List + HashMap.
- **LFU (Least Frequently Used)**: Implemented using nested Maps or Min-Heap + HashMap.

## Concurrency Considerations
- Reads and writes to the `ConcurrentHashMap` are thread-safe.
- However, updating the eviction data structure (like the Doubly Linked List for LRU) requires synchronization. In high-concurrency systems, using `ReentrantReadWriteLock` or fine-grained locking is necessary to prevent bottlenecks.
- TTL expiration can be handled lazily (on `get`) or actively via a background cleanup thread.
