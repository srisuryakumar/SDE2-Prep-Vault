---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 12 — LLD Design 8 — Hotel Booking System"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Strategy Pattern", "Concurrency"]
tags: [lld, case-study, hotel, concurrency]
---

# LLD Case Study: Hotel Booking System

## Problem Overview
Design a system where guests can search hotels, view room availability, book rooms, and cancel bookings. The primary challenge is the **Concurrency Problem**: preventing two guests from booking the exact same room for overlapping dates simultaneously.

## Core Entities
- **Hotel:** Collection of Rooms.
- **Room:** A physical room with type (Standard, Suite) and base price.
- **RoomAvailability / RoomBooking:** Tracks the dates a room is booked.
- **Guest:** The user.
- **PricingStrategy:** Handles seasonal/weekend pricing logic.
- **CancellationPolicy:** Handles refund calculations.

## The Concurrency Solution (Optimistic Locking)
The classic problem: Two users look at the last available room on the same dates. Both see it as available. Both click "Book" at the same time.

### How Optimistic Locking Prevents Double Booking:
1. **The Database Schema:** Have a `room_availability` table with a `@Version` column.
2. **The Read:** Both transactions read the availability rows for their date range. Let's say `version = 1`.
3. **The Validation:** Both transactions confirm the dates are available in memory.
4. **The Write (Update):** Both transactions attempt to book the room. The ORM (like Hibernate) generates SQL like:
   ```sql
   UPDATE room_availability SET available = false, version = version + 1
   WHERE id = 123 AND version = 1;
   ```
5. **The Conflict:**
   - Thread A's UPDATE succeeds (`rowsAffected = 1`). `version` becomes `2`.
   - Thread B's UPDATE executes a millisecond later: `WHERE id = 123 AND version = 1`. Because the version is now `2`, it finds `0` rows.
6. **The Result:** Thread B throws an `OptimisticLockException` (or `ObjectOptimisticLockingFailureException` in Spring). Thread B's transaction rolls back. The user receives an error: "This room was just booked by someone else."

## Pricing Strategy (Strategy Pattern)
Pricing isn't static. It changes based on weekends, holidays, or early bird discounts.
Create a `PricingStrategy` interface:
- `StandardPricingStrategy` (adds 30% for weekends)
- `EarlyBirdPricingStrategy` (decorator/wrapper that applies a 15% discount if booked > 30 days in advance).

To compute the price, the Strategy iterates through every single day between `checkIn` and `checkOut` and sums the daily calculated rate.
