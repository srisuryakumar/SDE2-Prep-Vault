---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 11 — Design 9 — BookMyShow"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, bookmyshow, concurrency, ticketing]
---

# HLD Case Study: BookMyShow (Ticketing/Flash Sales)

## Problem Overview
Handle high-concurrency flash sales (e.g. concert tickets).
- **Contention problem:** 50,000 seats vs 500,000 concurrent users trying to book at exactly the same time.
- **Constraint:** Zero double-booking.

## The Seat Availability Race Condition
If two users see seat A5 as available and click "book" simultaneously, a basic DB update allows a double booking.

### Step 1: Redis Hold (Fast Reservation)
```
SET seat:show123:A5 "userId_789" EX 600 NX
```
- `NX` = only set if key doesn't exist (atomic check-and-set).
- `EX 600` = 10 minute hold.
Redis is single-threaded, so this completely closes the race condition. If the user doesn't pay in 10 mins, the key automatically expires and the seat is released.

### Step 2: Database Confirmation (Payment Success)
Once payment succeeds, lock the row to permanently book it.
```sql
BEGIN;
SELECT * FROM seats WHERE show_id = 123 AND seat_id = 'A5' FOR UPDATE;
UPDATE seats SET status = 'booked', user_id = 789 WHERE ...;
COMMIT;
```
The `SELECT ... FOR UPDATE` acts as defense-in-depth, locking the DB row so no concurrent process can modify it.

## Flash Sale Architecture: Virtual Waiting Room
Allowing 500,000 users to hit the booking API instantly will crash Redis/Postgres.
Instead, route users to a **Virtual Waiting Room** via WebSockets. The system admits users in controlled batches matching backend capacity, turning a massive instantaneous spike into a steady, manageable stream.

## Common Questions
**Q: Why not just use `SELECT FOR UPDATE` directly instead of Redis holds?**
A: A 10-minute hold via `SELECT FOR UPDATE` would hold a DB row lock for the entire payment flow (10 minutes). DB connections/locks are scarce resources. Redis holds are cheap and self-expiring.

**Q: How do you keep the waiting room fair?**
A: Assign each entrant a monotonically increasing position token from a distributed atomic counter when they enter. Admit strictly by token order.
