---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 12 — Design 10 — Feed Generation"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Trade-offs"]
tags: [hld, case-study, feed, fan-out, social-network]
---

# HLD Case Study: Feed Generation (Instagram/Twitter)

## Problem Overview
Generate a personalized, reverse-chronological feed of posts from people a user follows.
- **Scale:** 300M DAU, ~6,000 posts/sec. Extreme power-law skew (some accounts have tens of millions of followers).
- **Read-heavy:** The feed is opened far more often than posts are created. Loads must be sub-second.

## Fan-Out Strategies

### 1. Fan-out on Write (Push)
When a user posts, immediately push the post ID into the precomputed feed (Redis list) of every follower.
- *Pros:* Feed reads are O(1) and extremely fast.
- *Cons:* A celebrity with 10M followers triggers **10M writes** for a single post (massive write amplification).

### 2. Fan-out on Read (Pull)
Don't precompute. When a user opens their feed, fetch the most recent posts from everyone they follow and merge them.
- *Pros:* No write amplification (posting is O(1)).
- *Cons:* Reading is expensive and slow.

## The Hybrid Approach (Production Solution)
Combine both strategies based on follower count.
- **For regular users (< 1M followers):** Use **Fan-out on Write**. Pushes to followers' precomputed Redis lists.
- **For celebrities (>= 1M followers):** Use **Fan-out on Read**. Do NOT push their posts to followers' lists.
- **Feed Read:**
  1. Read the precomputed Redis list (covers regular followed users).
  2. Separately fetch recent posts from the handful of celebrities the user follows.
  3. Merge and rank.

This provides O(1) reads for the vast majority of posts while avoiding the celebrity write-storm.

## Handling 10x Scale
- **Fan-out Workers:** Shard the fan-out work across many workers by follower-ID range.
- **Redis Feed Lists:** Shard by user ID. Cap the feed list length (e.g., last 800 posts).
- Tune the celebrity threshold dynamically based on fan-out worker capacity.

## Common Questions
**Q: What if a user unfollows someone after a post was fanned out?**
A: Don't retroactively remove it from the Redis list (too complex). Instead, filter it at read/render time, or just let it scroll out naturally.
