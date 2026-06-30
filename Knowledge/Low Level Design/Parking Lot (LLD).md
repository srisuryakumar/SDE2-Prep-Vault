---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 5 — LLD Design 1 — Parking Lot"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Strategy Pattern", "Singleton Pattern"]
tags: [lld, case-study, parking-lot]
---

# LLD Case Study: Parking Lot

## Problem Overview
Design a parking lot with multiple floors, different vehicle types (Motorcycle, Car, Truck), different spot sizes (Small, Medium, Large), and variable pricing strategies. Must handle concurrent entry and exit safely.

## Core Entities
- **ParkingLot:** The central singleton coordinating entry and exit.
- **Floor:** Contains a collection of spots.
- **ParkingSpot:** Holds size, occupancy status, and current vehicle.
- **Vehicle:** Abstract base class (`Car`, `Motorcycle`, `Truck`) defining compatible spot sizes.
- **Ticket:** Issued on entry, used for billing.
- **PricingStrategy:** Interface for calculating cost (Hourly, DailyCap, Weekend).

## Design Patterns Used
1. **Singleton:** `ParkingLot` (only one instance per building).
2. **Strategy:** `PricingStrategy` allows swapping hourly vs. weekend rates without modifying the core checkout logic.
3. **Template / Factory:** Often used for generating different ticket formats.

## Concurrency (The Tricky Part)
**The Race Condition:** Two cars enter simultaneously when only 1 medium spot remains. Both threads call `findAndOccupySpot`, see the spot as available, and attempt to occupy it.

**Solutions:**
1. **Pessimistic Locking (Simple):** Make `findAndOccupySpot()` a `synchronized` method on the `ParkingLot` object. This serializes all entries. Safe, but creates a bottleneck at high volume.
2. **Finer-Grained Locking:** Lock on the `Floor` object rather than the entire parking lot, reducing contention.
3. **Lock-Free (Atomic):** Use `AtomicBoolean` for the `occupied` flag inside `ParkingSpot`. Threads call `occupied.compareAndSet(false, true)`. Only one thread will succeed.

## Extensibility
- **Adding an Electric Bike:** Add `ElectricBike extends Vehicle` and maybe `ELECTRIC_SMALL` to `SpotType`. No changes to `ParkingLot`. (Open/Closed Principle).
- **Distributed System:** Replace the in-memory `ConcurrentHashMap` of active tickets with Redis, and use Redis `SET NX` for atomic spot reservations across multiple app instances.
