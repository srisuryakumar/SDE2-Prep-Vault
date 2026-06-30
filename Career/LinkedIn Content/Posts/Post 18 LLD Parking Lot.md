---
type: linkedin-post
post_number: 18
scheduled_week: 9
scheduled_day: Friday
status: drafted
---
Parking Lot LLD — here's the full class diagram and every design decision.

GitHub: [link to lld-java/parking-lot]

[ATTACH: Class diagram image]

Design decisions:

1. Singleton for ParkingLot
   There is only one parking lot. getInstance() enforces this.

2. Strategy Pattern for Pricing
   HourlyPricingStrategy, DailyPricingStrategy, WeekendPricingStrategy.
   Adding a new pricing model = new class, zero changes to ParkingLot.

3. Vehicle hierarchy
   Abstract Vehicle → Car, Truck, Motorcycle.
   Each knows its size. ParkingSpot knows its capacity.

4. The concurrency problem (most interviewers ask this):
   Two cars arrive simultaneously for the last available spot.
   Solution: synchronized findAndOccupySpot() method.
   Or for production: SELECT FOR UPDATE on the spot row in PostgreSQL.

5. What I'd do differently at scale:
   Replace in-memory HashMap of spots with Redis.
   This makes it work across multiple parking lot service instances.

#LLD #Java #BackendEngineering
