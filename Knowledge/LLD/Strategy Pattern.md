---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 4 — Behavioral Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["State Pattern"]
tags: [lld, design-patterns, behavioral]
---

# Strategy Pattern

## Intuition
When you have multiple algorithms (or variations of logic) for the same task, and you see massive `if/else` or `switch` chains (e.g., pricing rules based on customer type), you need Strategy.

## The Solution
1. Define a `Strategy` interface (e.g., `PricingStrategy`).
2. Implement each algorithm in its own concrete class (`RegularPricingStrategy`, `PremiumPricingStrategy`).
3. The Context (`PricingEngine`) holds a reference to the Interface and delegates the computation to it.
4. The specific strategy is injected by the client at runtime (often via a Factory or Registry).

**Real-world Examples:**
- Cache Eviction Policies (LRU vs LFU).
- Sorting Algorithms.
- Pricing Engines.

**Strategy vs State:**
- Strategy: The algorithm is chosen by the *client* at construction or call time. The context is stateless about which strategy to use.
- State: The object transitions between states *autonomously* based on internal logic.
