# Chapter 13: LLD Interview Strategy

> "The interviewer isn't grading your final code. They're watching how you think."

---

## The 45-Minute Framework

Most LLD interviews run 45–60 minutes. Here is exactly how to allocate that time.

```
Minutes  0–5   : Requirements clarification
Minutes  5–10  : Entity identification and responsibilities
Minutes 10–20  : Class relationships, UML sketch on whiteboard/paper
Minutes 20–40  : Core implementation (code)
Minutes 40–45  : Edge cases, concurrency, extensibility discussion
```

---

## Phase 1: Requirements (5 minutes)

**Never skip this.** The single most common mistake is jumping to code before understanding what you're building.

Ask these questions regardless of what the problem is:

```
Functional scope:
□ What are the top 3 operations users perform?
□ Are there different user roles? (admin, member, guest)
□ What is the scale? (100 users or 100M users?)
□ Should I handle [specific edge case]? (out of stock, expired session, etc.)

Non-functional constraints:
□ Is consistency more important than availability?
□ Should I optimize for read or write performance?
□ Is this single-machine or distributed?

Simplifications you can propose:
□ "I'll assume no authentication — just focus on core booking logic. Is that OK?"
□ "I'll skip payment processing details and assume it succeeds. Should I model it?"
□ "I'll ignore persistence and implement in-memory first."
```

**Interviewers WANT you to ask these.** It shows seniority. Junior candidates dive into code. Senior candidates clarify before they write a line.

---

## Phase 2: Entity Identification (5 minutes)

Write nouns, not code. On the whiteboard, list the key entities.

**How to find entities:**
1. Read back the requirements in your own words
2. Every noun in your description is a candidate entity
3. Ask: Does this noun have meaningful attributes AND behaviors? If yes, it's an entity.

**Example — Parking Lot requirements → entities:**

> "Vehicles enter, get a spot assigned, and pay when they leave."

| Noun | Entity? | Why |
|------|---------|-----|
| Vehicle | ✅ | Has type, license plate; behavior: fits in spots |
| Spot | ✅ | Has type, floor, occupation state |
| Ticket | ✅ | Has entry time, vehicle, spot |
| Payment | ✅ | Has amount, time, method |
| Floor | ✅ | Has a list of spots |
| ParkingLot | ✅ | Top-level controller |
| Entry | ❌ | Not an entity — it's a method (vehicleEntry) |
| Charge | ❌ | Not an entity — it's computed by PricingStrategy |

**Verbalize your reasoning:**
> "I see three main actors: the Vehicle that enters, the ParkingSpot it occupies, and the Ticket that records the session. I'll also need a ParkingLot as the system controller and a PricingStrategy for flexible billing."

---

## Phase 3: Class Relationships (10 minutes)

Draw or describe:

```
1. INHERITANCE (IS-A):  
   Vehicle (abstract) → Car, Motorcycle, Truck
   Only use when truly all subclasses share the same contract.

2. COMPOSITION (HAS-A):
   ParkingLot HAS-A List<Floor>
   Floor HAS-A List<ParkingSpot>
   Ticket HAS-A Vehicle, ParkingSpot

3. INTERFACES (CAN-DO):
   Priceable → implemented by PricingStrategy
   Notifiable → implemented by EmailNotifier, SMSNotifier

4. DEPENDENCY (USES):
   ParkingLot USES PricingStrategy to calculate fees
```

**On the whiteboard, a 5-box UML sketch beats a wall of code:**

```
     ParkingLot ─── has ──► Floor[] ─── has ──► ParkingSpot[]
          │                                           │
     uses │                                      occupied by
          ▼                                           ▼
   PricingStrategy ◄── implements ──── Vehicle (Car/Truck/Motorcycle)
```

Describe it aloud:
> "ParkingLot is a Singleton. It contains floors, each with spots. A Vehicle maps to a spot via a Ticket. PricingStrategy is an interface so I can add new pricing rules without changing the core logic."

---

## Phase 4: Core Implementation (20 minutes)

Write the most important code first. What is "most important"?

**Priority 1: The central entity and its core behavior**
```java
// The class that everything revolves around
public class ParkingLot {
    public Ticket vehicleEntry(Vehicle vehicle) { ... }
    public Payment vehicleExit(String licensePlate) { ... }
}
```

**Priority 2: The interface / hierarchy**
```java
public abstract class Vehicle { ... }
public class Car extends Vehicle { ... }
```

**Priority 3: The design pattern that solves the key problem**
```java
// Strategy for pricing
public interface PricingStrategy { double calculate(Ticket t); }
// Observer for events
eventBus.publish(new OrderPlacedEvent(...));
```

**What to skip if time is short:**
- Getters/setters (say "I'll add the usual getters")
- Repository layer (say "this would hit a database in production")
- Full validation (say "I'll add null checks and boundary conditions")

**What to NEVER skip:**
- The interface definition (shows you thought about abstraction)
- The synchronization/locking on the critical path (shows concurrency awareness)
- The constructor with required fields (shows you thought about valid state)

---

## Phase 5: Edge Cases and Extensibility (5 minutes)

Close with a walk-through of:

**Concurrency:**
> "In the parking lot, two cars could try to take the last spot simultaneously. My `findAndOccupySpot` is synchronized, so only one thread can check-and-assign at a time."

**Extensibility (the interviewer's favorite):**
> "If we want to add electric vehicles with charging spots, I add an `ELECTRIC` SpotType and an `ElectricCar extends Vehicle` with `getCompatibleSpotTypes()` returning `[ELECTRIC, LARGE]`. No existing class changes."

**Failure cases:**
> "If payment fails during checkout, the ticket is not cleared and the spot stays occupied. I'd add a retry mechanism or a transaction-style rollback."

---

## Common Mistakes That Fail Candidates

### Mistake 1: No Requirements Clarification
```
Interviewer: "Design a food delivery system."
Bad candidate: [immediately opens IDE and starts writing FoodItem class]
Good candidate: "Before I start — can I ask a few questions? Are we building 
  the customer ordering side, the restaurant management side, or both? 
  Do we need real-time order tracking? What's the scale?"
```

### Mistake 2: No Abstraction — Only Concrete Classes

```java
// Bad — interviewer sees no OOP thinking
public class OrderService {
    public void placeStripeOrder() { ... }
    public void placeRazorpayOrder() { ... }
    public void placePayPalOrder() { ... }
}

// Good — demonstrates design thinking
public interface PaymentGateway { void charge(double amount); }
public class OrderService {
    private final PaymentGateway gateway;
    public void placeOrder(Order order) { gateway.charge(order.getTotal()); }
}
```

### Mistake 3: Ignoring Concurrency Entirely

Every LLD problem with real-world usage has a concurrency concern. Naming it — even if you don't have time to code it — scores points:
- Parking lot: two cars for last spot
- BookMyShow: two users selecting same seat
- ATM: two cards from the same account withdrawing simultaneously
- Library: two members borrowing the last copy

### Mistake 4: Over-Engineering Early

```
Bad: "I'll use a Visitor pattern, Chain of Responsibility for validation, 
     an Abstract Factory for the UI layer, and a Flyweight for seat objects..."
     [15 minutes in, no actual code written]

Good: Start with the simplest thing that works.
      Add patterns when you identify a specific pain point they solve.
```

### Mistake 5: Forgetting to Mention Trade-offs

Interviewers at SDE-2 level expect trade-off awareness:

```
"I used synchronized here for correctness. In a high-throughput system, 
 I'd replace this with an AtomicBoolean.compareAndSet() for lock-free 
 coordination, or delegate to Redis for distributed deployments."

"I used a simple List for the waitlist. For production, I'd use a 
 database queue to survive restarts."
```

---

## How to Handle "Design X I've Never Seen"

Some interviewers give obscure problems: "Design a stock exchange order book," "Design a URL shortener," "Design a vending machine for a hospital."

**The process is always the same:**

```
Step 1: Ask "What are the core operations?" (usually 3-5)
Step 2: Name the nouns → entities
Step 3: Find the single hardest constraint (concurrency? ordering? consistency?)
Step 4: Apply the pattern that solves that constraint
Step 5: Code the critical path, sketch the rest
```

**For "stock exchange order book":**
```
Operations: place bid, place ask, match orders, get order book
Core constraint: order matching must be atomic (race condition on matching)
Pattern: two priority queues (max-heap for bids, min-heap for asks) + synchronized matching
Critical path: match() — code this first
```

**For "hospital vending machine":**
```
Operations: authenticate staff, select item, dispense, log
Core constraint: state machine (idle → authenticated → item selected → dispensed)
Pattern: State pattern (same as vending machine from Chapter 4)
Critical path: state transitions — code this first
```

---

## Showing Extensibility: The Killer Phrase

Interviewers love hearing this structure:

> "Currently, I support X. If we need to add Y, I only need to Z, and none of the existing code changes."

**Examples:**
- "Currently, I support Stripe and Razorpay. If we add UPI, I only need to create a `UPIGateway implements PaymentGateway`. The `OrderService` and `PaymentProcessor` are unchanged."
- "Currently, I calculate fines per day. If we want per-week fines with a grace period, I create a new `PricingStrategy` implementation. The `LibraryService` doesn't change."
- "Currently, I notify by email. If we add WhatsApp, I subscribe a new listener to the event bus. `OrderService` never knows this happened."

This demonstrates OCP, DIP, and extensible design in one sentence.

---

## The SDE-2 vs SDE-1 Difference

Interviewers calibrate expectations. At SDE-2:

| Dimension | SDE-1 Expected | SDE-2 Expected |
|-----------|---------------|----------------|
| Patterns | Can implement when told | Independently identifies which pattern fits |
| Concurrency | Aware it exists | Identifies exact race condition, proposes solution |
| Trade-offs | "It works" | "This approach has X trade-off vs Y approach" |
| Extensibility | Adds new code correctly | Adds without modifying existing code |
| Requirements | Asks basic questions | Asks probing questions, challenges assumptions |
| Code quality | Correct and readable | Correct, readable, production-grade encapsulation |

---

## Quick-Reference: Pattern → When to Use in LLD

| You see this in the design... | Reach for this pattern |
|------------------------------|----------------------|
| Multiple concrete types doing the same operation | Strategy |
| Something happening that other things need to know about | Observer / Event Bus |
| Complex object with many optional fields | Builder |
| Only one instance should ever exist | Singleton |
| Different algorithms selected by type string | Factory Method |
| Behavior depends on object's current state | State |
| Validation/processing pipeline with early exit | Chain of Responsibility |
| Adding features to an existing class you can't modify | Decorator |
| Third-party API doesn't fit your interface | Adapter |
| Complex subsystem with a simple client interface | Facade |
| Tree structure of similar items | Composite |
| Request as an object (for undo/redo, queuing) | Command |
| Algorithm skeleton with varying steps | Template Method |

---

## Final Checklist Before Finishing Any LLD Interview

```
□ Did I ask for requirements? Did I confirm scope?
□ Did I name all the key entities and their responsibilities?
□ Did I use an interface/abstraction for each variation point?
□ Is the critical path coded (not just sketched)?
□ Did I mention concurrency? Did I show how to handle it?
□ Did I show extensibility with a concrete example?
□ Did I mention what I would do differently in production?
□ Did I talk through time complexity of the core operations?
```

---

## The Last Word

Every senior engineer you admire has a simple mental model under their complex code: **identify what changes, isolate it behind an interface, and make the rest of the system depend only on that interface.**

That's the entire point of design patterns.
That's the entire point of LLD interviews.

The question "how would you add a new vehicle type?" is just asking: did you put the right abstraction in the right place?

When you can answer every "how would you add X?" question with "create a new class, register it, done — no existing code changes," you have mastered LLD.
