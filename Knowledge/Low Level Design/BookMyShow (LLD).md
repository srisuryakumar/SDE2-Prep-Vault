---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 6 — LLD Design 2 — BookMyShow (Movie Ticket Booking)"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["State Pattern"]
tags: [lld, case-study, concurrency, bookmyshow]
---

# LLD Case Study: BookMyShow

## Problem Overview
Design a movie ticket booking system where users can browse shows, select seats, and book them. The primary challenge is the **Concurrency Problem**: preventing two users from double-booking the exact same seat at the exact same millisecond.

## Core Entities
- **Movie:** The title being shown.
- **Theatre / Screen:** The physical location.
- **Seat:** The physical seat configuration (e.g., A5, Premium).
- **Show:** A specific showing of a Movie on a Screen at a given time.
- **ShowSeat:** The stateful entity representing a Seat for a specific Show. Contains status (`AVAILABLE`, `HELD`, `BOOKED`).
- **Booking:** The transaction tracking the user, show, seats, and payment.

## The State Machine
```text
AVAILABLE ──── User selects ────► HELD (TTL: 10 min)
    ▲                                    │
    │                                    │ Payment succeeds
    │ TTL expires / User cancels         ▼
    └──────────────────────────── BOOKED
```
- **HELD:** Temporary reservation during the payment window. If payment fails or expires, it returns to `AVAILABLE`.
- **BOOKED:** Permanent state after successful payment.

## Concurrency Solutions (Preventing Double Booking)

### 1. In-Memory (Java-level)
Make `tryHold()` a `synchronized` method on the `ShowSeat` object. Only one thread can check if the seat is `AVAILABLE` and change it to `HELD`.

### 2. Database-Level (Production)
- **Optimistic Locking:** Add a `version` column to the `show_seats` table.
  ```sql
  UPDATE show_seats SET status = 'HELD', version = version + 1
  WHERE seat_id = 123 AND status = 'AVAILABLE' AND version = 1;
  ```
- **Pessimistic Locking:** `SELECT ... FOR UPDATE` locks the row until the transaction commits.

### 3. Distributed Cache / Redis (Flash Sales - 100K users)
Use Redis's atomic `SET NX` (Set if Not eXists) with a TTL for O(1) performance.
```java
// Redis SET seat:show123:A5 user456 EX 600 NX
redisTemplate.opsForValue().setIfAbsent(redisKey, userId, Duration.ofSeconds(600));
```
- Single-threaded execution ensures atomicity.
- TTL (Time To Live) automatically expires the hold after 10 minutes without a cron job.

## Handling Flash Sales (Scale)
1. **Rate Limiting:** At the API gateway to drop excessive requests.
2. **Queuing:** Queue incoming requests (Kafka/SQS) to smooth the spike.
3. **Redis Holds:** `SET NX` handles concurrent grabs.
4. **Caching:** Cache the seat map in Redis; don't query the DB on every page load.
5. **Circuit Breakers:** Prevent slow downstream payment gateways from cascading failures.
