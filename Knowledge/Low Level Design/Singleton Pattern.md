---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 2 — Creational Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, creational]
---

# Singleton Pattern

## Intuition
You need exactly *one* instance of a class, shared across the entire application (e.g., Database Connection Pool, Configuration Manager, Logger).

## The Evolution of Thread Safety
1. **Naive (Not Thread-Safe):** A simple `if (instance == null)` fails in multi-threaded environments because two threads can pass the null check simultaneously.
2. **Synchronized Method (Slow):** Making the entire `getInstance()` method `synchronized` is thread-safe, but creates a massive bottleneck because every caller acquires the lock even after initialization.
3. **Double-Checked Locking with `volatile` (Production-Grade):**
   ```java
   private static volatile ConfigManager instance;
   public static ConfigManager getInstance() {
       if (instance == null) {
           synchronized (ConfigManager.class) {
               if (instance == null) {
                   instance = new ConfigManager();
               }
           }
       }
       return instance;
   }
   ```
   `volatile` prevents the JVM from reordering the memory allocation and initialization steps.
4. **Enum Singleton (The Best Java Singleton):**
   ```java
   public enum ConfigManager {
       INSTANCE;
       // ... methods ...
   }
   ```
   The JVM guarantees a single instance per enum constant. It is thread-safe, immune to reflection attacks, and immune to serialization attacks.

*Note: In Spring Boot, beans are singletons by default, so you rarely implement this manually.*
