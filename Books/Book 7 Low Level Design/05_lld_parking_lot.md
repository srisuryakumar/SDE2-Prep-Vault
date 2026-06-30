# Chapter 5: LLD Design 1 — Parking Lot

> "How would you design a parking lot?" is the most common LLD warm-up question. It tests entity modeling, concurrency awareness, and pattern application all at once.

---

## Step 1: Requirements Gathering (5 minutes)

Clarify scope before writing any code. Ask the interviewer:

**Functional Requirements:**
- Multiple floors, each with a configurable number of spots
- Multiple vehicle types: motorcycles, cars, trucks/buses
- Different spot sizes: SMALL, MEDIUM, LARGE
- Entry: find and assign the nearest available spot
- Exit: release spot, calculate charges, generate receipt
- Concurrent entry/exit: many vehicles simultaneously

**Non-Functional Requirements:**
- Correctness: no two vehicles assigned the same spot
- The system must handle race conditions on the last available spot

**Constraints/Assumptions:**
- A vehicle can only park in a spot of matching or larger size
- Pricing is configurable (hourly, daily, weekend rates)
- One parking lot (multi-floor, single building) — not a distributed system

---

## Step 2: Identify Entities

```
ParkingLot        — top-level, singleton
├── Floor[]       — each floor has spots
│   └── ParkingSpot[] — individual spots
Vehicle           — abstract, subtypes: Car, Motorcycle, Truck
Ticket            — issued on entry, used for billing on exit
Payment           — result of billing calculation
PricingStrategy   — interface for rate calculation
```

---

## Step 3: Class Hierarchy (UML Description)

```
Vehicle (abstract)
    ├── Car          extends Vehicle
    ├── Motorcycle   extends Vehicle
    └── Truck        extends Vehicle

SpotType (enum): SMALL, MEDIUM, LARGE

ParkingSpot
    ├── spotId: String
    ├── floor: int
    ├── type: SpotType
    ├── occupied: boolean (volatile)
    └── currentVehicle: Vehicle

ParkingLot (Singleton)
    ├── floors: List<Floor>
    └── findAndOccupySpot(Vehicle): Optional<ParkingSpot>  ← synchronized

Floor
    ├── floorNumber: int
    └── spots: List<ParkingSpot>

Ticket
    ├── ticketId: String
    ├── vehicle: Vehicle
    ├── spot: ParkingSpot
    ├── entryTime: LocalDateTime
    └── exitTime: LocalDateTime

PricingStrategy (interface)
    ├── HourlyPricingStrategy
    ├── DailyCapPricingStrategy
    └── WeekendPricingStrategy

Payment
    ├── ticket: Ticket
    ├── amount: double
    └── paymentTime: LocalDateTime
```

---

## Step 4: Full Java Implementation

```java
// ── Vehicle Hierarchy ──────────────────────────────────────────────────────

public enum VehicleType {
    MOTORCYCLE, CAR, TRUCK
}

public abstract class Vehicle {
    private final String licensePlate;
    private final VehicleType type;

    protected Vehicle(String licensePlate, VehicleType type) {
        this.licensePlate = licensePlate;
        this.type         = type;
    }

    public String getLicensePlate() { return licensePlate; }
    public VehicleType getType()    { return type; }

    // Each vehicle knows what spot sizes fit it
    public abstract List<SpotType> getCompatibleSpotTypes();

    @Override
    public String toString() {
        return type + "[" + licensePlate + "]";
    }
}

public class Motorcycle extends Vehicle {
    public Motorcycle(String licensePlate) {
        super(licensePlate, VehicleType.MOTORCYCLE);
    }

    @Override
    public List<SpotType> getCompatibleSpotTypes() {
        return List.of(SpotType.SMALL, SpotType.MEDIUM, SpotType.LARGE);
    }
}

public class Car extends Vehicle {
    public Car(String licensePlate) {
        super(licensePlate, VehicleType.CAR);
    }

    @Override
    public List<SpotType> getCompatibleSpotTypes() {
        return List.of(SpotType.MEDIUM, SpotType.LARGE);
    }
}

public class Truck extends Vehicle {
    public Truck(String licensePlate) {
        super(licensePlate, VehicleType.TRUCK);
    }

    @Override
    public List<SpotType> getCompatibleSpotTypes() {
        return List.of(SpotType.LARGE);
    }
}
```

```java
// ── Parking Spot ──────────────────────────────────────────────────────────

public enum SpotType {
    SMALL, MEDIUM, LARGE
}

public class ParkingSpot {
    private final String spotId;       // e.g., "F1-S05"
    private final int floor;
    private final SpotType type;
    private volatile boolean occupied; // volatile for visibility across threads
    private Vehicle currentVehicle;

    public ParkingSpot(String spotId, int floor, SpotType type) {
        this.spotId   = spotId;
        this.floor    = floor;
        this.type     = type;
        this.occupied = false;
    }

    public String getSpotId()          { return spotId; }
    public int getFloor()              { return floor; }
    public SpotType getType()          { return type; }
    public boolean isOccupied()        { return occupied; }
    public Vehicle getCurrentVehicle() { return currentVehicle; }

    // Package-private — only ParkingLot should call these
    synchronized void occupy(Vehicle vehicle) {
        if (occupied) throw new IllegalStateException("Spot " + spotId + " is already occupied");
        this.currentVehicle = vehicle;
        this.occupied       = true;
    }

    synchronized void vacate() {
        this.currentVehicle = null;
        this.occupied       = false;
    }

    @Override
    public String toString() {
        return spotId + "(" + type + (occupied ? ",OCCUPIED" : ",FREE") + ")";
    }
}
```

```java
// ── Floor ────────────────────────────────────────────────────────────────

public class Floor {
    private final int floorNumber;
    private final List<ParkingSpot> spots;

    public Floor(int floorNumber, List<ParkingSpot> spots) {
        this.floorNumber = floorNumber;
        this.spots       = new ArrayList<>(spots);
    }

    public int getFloorNumber() { return floorNumber; }

    public List<ParkingSpot> getAvailableSpots(List<SpotType> compatibleTypes) {
        return spots.stream()
            .filter(spot -> !spot.isOccupied() && compatibleTypes.contains(spot.getType()))
            .collect(java.util.stream.Collectors.toList());
    }

    public long countAvailable() {
        return spots.stream().filter(s -> !s.isOccupied()).count();
    }

    public long countTotal() { return spots.size(); }
}
```

```java
// ── Ticket ────────────────────────────────────────────────────────────────

public class Ticket {
    private final String ticketId;
    private final Vehicle vehicle;
    private final ParkingSpot spot;
    private final LocalDateTime entryTime;
    private LocalDateTime exitTime;

    public Ticket(Vehicle vehicle, ParkingSpot spot) {
        this.ticketId  = "TKT-" + System.currentTimeMillis();
        this.vehicle   = vehicle;
        this.spot      = spot;
        this.entryTime = LocalDateTime.now();
    }

    public void markExit() { this.exitTime = LocalDateTime.now(); }

    public String getTicketId()         { return ticketId; }
    public Vehicle getVehicle()         { return vehicle; }
    public ParkingSpot getSpot()        { return spot; }
    public LocalDateTime getEntryTime() { return entryTime; }
    public LocalDateTime getExitTime()  { return exitTime; }

    public long getDurationMinutes() {
        LocalDateTime end = exitTime != null ? exitTime : LocalDateTime.now();
        return java.time.Duration.between(entryTime, end).toMinutes();
    }
}
```

```java
// ── Pricing Strategy ─────────────────────────────────────────────────────

public interface PricingStrategy {
    double calculate(Ticket ticket);
    String getStrategyName();
}

public class HourlyPricingStrategy implements PricingStrategy {
    private final Map<SpotType, Double> hourlyRates;

    public HourlyPricingStrategy() {
        hourlyRates = new EnumMap<>(SpotType.class);
        hourlyRates.put(SpotType.SMALL,  20.0);  // ₹20/hour
        hourlyRates.put(SpotType.MEDIUM, 40.0);  // ₹40/hour
        hourlyRates.put(SpotType.LARGE,  80.0);  // ₹80/hour
    }

    @Override
    public double calculate(Ticket ticket) {
        long minutes = ticket.getDurationMinutes();
        double hours = Math.ceil(minutes / 60.0); // round up to next hour
        double rate  = hourlyRates.getOrDefault(ticket.getSpot().getType(), 40.0);
        return hours * rate;
    }

    @Override
    public String getStrategyName() { return "HOURLY"; }
}

public class DailyCapPricingStrategy implements PricingStrategy {
    private static final double DAILY_CAP = 500.0; // ₹500 max per day
    private final PricingStrategy hourlyStrategy;

    public DailyCapPricingStrategy() {
        this.hourlyStrategy = new HourlyPricingStrategy();
    }

    @Override
    public double calculate(Ticket ticket) {
        double hourlyCharge = hourlyStrategy.calculate(ticket);
        long days = Math.max(1, (long) Math.ceil(ticket.getDurationMinutes() / (60.0 * 24)));
        return Math.min(hourlyCharge, days * DAILY_CAP);
    }

    @Override
    public String getStrategyName() { return "DAILY_CAP"; }
}

public class WeekendPricingStrategy implements PricingStrategy {
    private final PricingStrategy weekdayStrategy;
    private static final double WEEKEND_MULTIPLIER = 1.5;

    public WeekendPricingStrategy(PricingStrategy weekdayStrategy) {
        this.weekdayStrategy = weekdayStrategy;
    }

    @Override
    public double calculate(Ticket ticket) {
        double base = weekdayStrategy.calculate(ticket);
        DayOfWeek day = ticket.getEntryTime().getDayOfWeek();
        boolean isWeekend = (day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY);
        return isWeekend ? base * WEEKEND_MULTIPLIER : base;
    }

    @Override
    public String getStrategyName() { return "WEEKEND_PREMIUM"; }
}
```

```java
// ── Payment ───────────────────────────────────────────────────────────────

public class Payment {
    private final String paymentId;
    private final Ticket ticket;
    private final double amount;
    private final LocalDateTime paymentTime;

    public Payment(Ticket ticket, double amount) {
        this.paymentId   = "PAY-" + System.currentTimeMillis();
        this.ticket      = ticket;
        this.amount      = amount;
        this.paymentTime = LocalDateTime.now();
    }

    public String getPaymentId()            { return paymentId; }
    public Ticket getTicket()               { return ticket; }
    public double getAmount()               { return amount; }
    public LocalDateTime getPaymentTime()   { return paymentTime; }

    @Override
    public String toString() {
        return String.format("Payment{id=%s, ticket=%s, amount=₹%.2f, time=%s}",
            paymentId, ticket.getTicketId(), amount, paymentTime);
    }
}
```

```java
// ── Parking Lot (Singleton + Core Logic) ─────────────────────────────────

public class ParkingLot {
    // Double-checked locking singleton
    private static volatile ParkingLot instance;

    private final String name;
    private final List<Floor> floors;
    private final PricingStrategy pricingStrategy;
    private final Map<String, Ticket> activeTickets; // licencePlate → Ticket

    private ParkingLot(String name, List<Floor> floors, PricingStrategy pricingStrategy) {
        this.name            = name;
        this.floors          = new ArrayList<>(floors);
        this.pricingStrategy = pricingStrategy;
        this.activeTickets   = new ConcurrentHashMap<>();
    }

    public static ParkingLot getInstance() {
        if (instance == null) {
            synchronized (ParkingLot.class) {
                if (instance == null) {
                    instance = buildDefaultParkingLot();
                }
            }
        }
        return instance;
    }

    // Package-private for testing — allows resetting the singleton
    static void resetInstance() { instance = null; }

    private static ParkingLot buildDefaultParkingLot() {
        List<Floor> floors = new ArrayList<>();
        for (int f = 1; f <= 3; f++) {
            List<ParkingSpot> spots = new ArrayList<>();
            for (int s = 1; s <= 10; s++) {
                spots.add(new ParkingSpot("F" + f + "-S" + String.format("%02d", s),
                    f, SpotType.SMALL));
            }
            for (int s = 11; s <= 25; s++) {
                spots.add(new ParkingSpot("F" + f + "-M" + String.format("%02d", s),
                    f, SpotType.MEDIUM));
            }
            for (int s = 26; s <= 30; s++) {
                spots.add(new ParkingSpot("F" + f + "-L" + String.format("%02d", s),
                    f, SpotType.LARGE));
            }
            floors.add(new Floor(f, spots));
        }
        PricingStrategy strategy = new WeekendPricingStrategy(new HourlyPricingStrategy());
        return new ParkingLot("City Center Parking", floors, strategy);
    }

    // ─── Entry ──────────────────────────────────────────────────────────

    public Ticket vehicleEntry(Vehicle vehicle) {
        if (activeTickets.containsKey(vehicle.getLicensePlate())) {
            throw new IllegalStateException("Vehicle " + vehicle.getLicensePlate()
                + " is already parked");
        }

        ParkingSpot spot = findAndOccupySpot(vehicle)
            .orElseThrow(() -> new RuntimeException("No available spot for " + vehicle));

        Ticket ticket = new Ticket(vehicle, spot);
        activeTickets.put(vehicle.getLicensePlate(), ticket);

        System.out.printf("✅ Entry: %s → Spot %s (Floor %d)  Ticket: %s%n",
            vehicle, spot.getSpotId(), spot.getFloor(), ticket.getTicketId());
        return ticket;
    }

    // CRITICAL: synchronized to prevent two threads from assigning the same spot
    private synchronized Optional<ParkingSpot> findAndOccupySpot(Vehicle vehicle) {
        List<SpotType> compatibleTypes = vehicle.getCompatibleSpotTypes();

        for (Floor floor : floors) {
            List<ParkingSpot> available = floor.getAvailableSpots(compatibleTypes);
            if (!available.isEmpty()) {
                ParkingSpot spot = available.get(0); // first available
                spot.occupy(vehicle);
                return Optional.of(spot);
            }
        }
        return Optional.empty();
    }

    // ─── Exit ───────────────────────────────────────────────────────────

    public Payment vehicleExit(String licensePlate) {
        Ticket ticket = activeTickets.remove(licensePlate);
        if (ticket == null) {
            throw new IllegalArgumentException("No active ticket for plate: " + licensePlate);
        }

        ticket.markExit();
        ticket.getSpot().vacate();

        double amount = pricingStrategy.calculate(ticket);
        Payment payment = new Payment(ticket, amount);

        System.out.printf("🚗 Exit: %s | Spot: %s | Duration: %d min | Amount: ₹%.2f%n",
            licensePlate, ticket.getSpot().getSpotId(),
            ticket.getDurationMinutes(), amount);

        return payment;
    }

    // ─── Availability Display ───────────────────────────────────────────

    public void displayAvailability() {
        System.out.println("\n═══════════════════════════════════════");
        System.out.println("  " + name + " — Availability");
        System.out.println("═══════════════════════════════════════");
        for (Floor floor : floors) {
            System.out.printf("  Floor %d: %d/%d spots available%n",
                floor.getFloorNumber(), floor.countAvailable(), floor.countTotal());
        }
        System.out.println("═══════════════════════════════════════\n");
    }

    public String getName() { return name; }
}
```

```java
// ── Demo / Main ───────────────────────────────────────────────────────────

public class ParkingLotDemo {
    public static void main(String[] args) throws InterruptedException {
        ParkingLot lot = ParkingLot.getInstance();
        lot.displayAvailability();

        Vehicle car1  = new Car("KA-01-AB-1234");
        Vehicle car2  = new Car("KA-01-CD-5678");
        Vehicle moto1 = new Motorcycle("MH-02-EF-9012");
        Vehicle truck = new Truck("DL-03-GH-3456");

        Ticket t1 = lot.vehicleEntry(car1);
        Ticket t2 = lot.vehicleEntry(car2);
        Ticket t3 = lot.vehicleEntry(moto1);
        Ticket t4 = lot.vehicleEntry(truck);
        lot.displayAvailability();

        // Simulate 2 hours passing (in real system, time elapses naturally)
        // For demo: Thread.sleep(7200000) — we'll just directly test exit
        Payment p1 = lot.vehicleExit(car1.getLicensePlate());
        System.out.println(p1);

        lot.displayAvailability();

        // Concurrent entry simulation
        simulateConcurrentEntry(lot);
    }

    private static void simulateConcurrentEntry(ParkingLot lot) throws InterruptedException {
        System.out.println("\n=== Simulating Concurrent Entry ===");
        List<Thread> threads = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            final int idx = i;
            threads.add(new Thread(() -> {
                try {
                    Car car = new Car("TEST-" + String.format("%03d", idx));
                    lot.vehicleEntry(car);
                } catch (Exception e) {
                    System.out.println("Thread " + idx + " failed: " + e.getMessage());
                }
            }));
        }
        threads.forEach(Thread::start);
        for (Thread t : threads) t.join();
        lot.displayAvailability();
    }
}
```

---

## Step 5: Concurrency Deep Dive

**The Race Condition Scenario:**
1. Spot F1-M11 is the last available medium spot
2. Thread A (Car KA-123): calls `findAndOccupySpot` → sees F1-M11 as available
3. Thread B (Car MH-456): calls `findAndOccupySpot` → also sees F1-M11 as available (before A occupies it)
4. Both threads call `spot.occupy()` → one must fail

**How our design handles it:**

```java
// Layer 1: synchronized method ensures only one thread scans and assigns at a time
private synchronized Optional<ParkingSpot> findAndOccupySpot(Vehicle vehicle) {
    // Only one thread is in here at any moment
    // ...
}

// Layer 2: ParkingSpot.occupy() is also synchronized as a safety net
synchronized void occupy(Vehicle vehicle) {
    if (occupied) throw new IllegalStateException("Spot already occupied");
    // ...
}

// The synchronized keyword on findAndOccupySpot serializes ALL spot assignments.
// This is correct but creates a bottleneck at high volume.
```

**For High-Volume Systems (Production):**

```java
// Better approach: per-floor locking reduces contention
private Optional<ParkingSpot> findAndOccupySpot(Vehicle vehicle) {
    for (Floor floor : floors) {
        synchronized (floor) {  // lock per floor, not the whole lot
            List<ParkingSpot> available = floor.getAvailableSpots(vehicle.getCompatibleSpotTypes());
            if (!available.isEmpty()) {
                ParkingSpot spot = available.get(0);
                spot.occupy(vehicle);
                return Optional.of(spot);
            }
        }
    }
    return Optional.empty();
}

// Even better: use AtomicBoolean for lock-free spot reservation
public class ParkingSpot {
    private final AtomicBoolean occupied = new AtomicBoolean(false);

    public boolean tryOccupy(Vehicle vehicle) {
        // compareAndSet: only succeeds for ONE thread when multiple try simultaneously
        if (occupied.compareAndSet(false, true)) {
            this.currentVehicle = vehicle;
            return true;
        }
        return false; // another thread won the race
    }
}
```

---

## Interview Questions

**Q: How do you handle two cars simultaneously trying to enter when only one spot remains?**

A: The `findAndOccupySpot` method is `synchronized` on the `ParkingLot` instance. Only one thread enters this method at a time. The first thread finds the spot and calls `spot.occupy()`. The second thread enters after the first exits, now sees no available spots, and gets `Optional.empty()`. For higher throughput, we can use per-floor locking or `AtomicBoolean.compareAndSet()` for lock-free spot reservation.

**Q: How would you add a new vehicle type, say an electric bike?**

A: Create `ElectricBike extends Vehicle`, implement `getCompatibleSpotTypes()` returning `[SMALL]`, and optionally add an `ELECTRIC_SMALL` SpotType enum value. No changes to `ParkingLot`, `Floor`, or `Ticket`. Open/Closed Principle holds.

**Q: How would you change the pricing model?**

A: Create a new `PricingStrategy` implementation (e.g., `HourByHourPricingStrategy` or `EventDayPricingStrategy`) and inject it into `ParkingLot`. The `Ticket` and `Payment` classes are unaffected. Strategy Pattern at work.

**Q: How would you scale this to a distributed system with multiple parking lot buildings?**

A: Replace the in-memory `ConcurrentHashMap` with a distributed cache (Redis). Use `SET spot:F1-M11 carId EX 3600 NX` for atomic spot reservation (NX = only if not exists). The parking lot becomes a service, and spot state is stored in Redis rather than in-process memory.

**Q: How would you add a reservation system (book a spot in advance)?**

A: Add a `Reservation` entity with `vehiclePlate`, `spotId`, `startTime`, `endTime`. Add a `RESERVED` state to `ParkingSpot`. During `findAndOccupySpot`, check for reservations and honor them. Use a scheduled job to release expired reservations.
