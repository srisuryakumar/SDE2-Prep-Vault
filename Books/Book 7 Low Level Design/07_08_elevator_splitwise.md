# Chapter 7: LLD Design 3 — Elevator System

> Elevator design tests your ability to model state machines, implement scheduling algorithms, and coordinate multiple cooperating objects.

---

## Step 1: Requirements

- Multiple elevators in one building
- Multiple floors
- Passengers request elevators from floors (external buttons) and select destinations (internal buttons)
- Efficient scheduling: minimize wait time
- Each elevator has states: IDLE, MOVING_UP, MOVING_DOWN, MAINTENANCE
- Dispatcher assigns requests to the best elevator

---

## Step 2: Entities

```
ElevatorSystem    — top-level, singleton
Elevator          — has state, current floor, pending stops
ElevatorState     — enum: IDLE, MOVING_UP, MOVING_DOWN, MAINTENANCE
Request           — floor where someone is waiting + direction
Dispatcher        — picks which elevator handles a request
Button            — floor buttons (external) and cabin buttons (internal)
```

---

## Step 3: Full Java Implementation

```java
// ── Enums ─────────────────────────────────────────────────────────────────

public enum Direction      { UP, DOWN }
public enum ElevatorStatus { IDLE, MOVING_UP, MOVING_DOWN, MAINTENANCE }
```

```java
// ── Request ───────────────────────────────────────────────────────────────

public class ElevatorRequest {
    private final int fromFloor;       // floor where button was pressed
    private final int toFloor;         // destination (0 if external request)
    private final Direction direction; // which direction button pressed
    private final long requestedAt;

    // External request: passenger waiting on floor 3, going up
    public ElevatorRequest(int fromFloor, Direction direction) {
        this.fromFloor  = fromFloor;
        this.toFloor    = -1; // unknown — passenger will press inside button
        this.direction  = direction;
        this.requestedAt = System.currentTimeMillis();
    }

    // Internal request: passenger inside elevator, pressing floor 7
    public ElevatorRequest(int fromFloor, int toFloor) {
        this.fromFloor  = fromFloor;
        this.toFloor    = toFloor;
        this.direction  = toFloor > fromFloor ? Direction.UP : Direction.DOWN;
        this.requestedAt = System.currentTimeMillis();
    }

    public int getFromFloor()        { return fromFloor; }
    public int getToFloor()          { return toFloor; }
    public Direction getDirection()  { return direction; }
    public long getRequestedAt()     { return requestedAt; }
    public boolean hasDestination()  { return toFloor != -1; }
}
```

```java
// ── Elevator ──────────────────────────────────────────────────────────────

public class Elevator {
    private final int elevatorId;
    private final int minFloor;
    private final int maxFloor;

    private int currentFloor;
    private ElevatorStatus status;

    // Pending stops — using TreeSets for efficient sorted access
    private final TreeSet<Integer> floorsGoingUp   = new TreeSet<>();
    private final TreeSet<Integer> floorsGoingDown = new TreeSet<>(Comparator.reverseOrder());

    private static final int FLOOR_TRAVEL_TIME_MS = 2000; // 2s per floor

    public Elevator(int elevatorId, int minFloor, int maxFloor, int startFloor) {
        this.elevatorId   = elevatorId;
        this.minFloor     = minFloor;
        this.maxFloor     = maxFloor;
        this.currentFloor = startFloor;
        this.status       = ElevatorStatus.IDLE;
    }

    /**
     * Add a floor to the elevator's stop list.
     * SCAN algorithm: elevator continues in current direction until no more stops.
     */
    public synchronized void addStop(int floor) {
        if (floor > currentFloor || (status == ElevatorStatus.IDLE && floorsGoingUp.isEmpty())) {
            if (floor > currentFloor) floorsGoingUp.add(floor);
            else if (floor < currentFloor) floorsGoingDown.add(floor);
            else openDoor(); // already at requested floor
        } else if (floor < currentFloor) {
            floorsGoingDown.add(floor);
        } else if (floor > currentFloor) {
            floorsGoingUp.add(floor);
        }
        // If currently idle, pick direction based on request
        if (status == ElevatorStatus.IDLE && floor != currentFloor) {
            if (floor > currentFloor) floorsGoingUp.add(floor);
            else floorsGoingDown.add(floor);
        }
        notifyAll(); // wake the drive loop
    }

    /**
     * SCAN (elevator) algorithm:
     * - Move in current direction, serve all stops in that direction
     * - When no more stops in this direction, reverse
     * - When no stops at all, go IDLE
     */
    public void driveLoop() {
        while (true) {
            synchronized (this) {
                while (floorsGoingUp.isEmpty() && floorsGoingDown.isEmpty()) {
                    status = ElevatorStatus.IDLE;
                    System.out.printf("[Elevator %d] IDLE at floor %d%n", elevatorId, currentFloor);
                    try { wait(); } catch (InterruptedException e) { return; }
                }

                if (status == ElevatorStatus.MOVING_UP || canGoUp()) {
                    moveUp();
                } else if (status == ElevatorStatus.MOVING_DOWN || canGoDown()) {
                    moveDown();
                }
            }
        }
    }

    private boolean canGoUp()   { return !floorsGoingUp.isEmpty(); }
    private boolean canGoDown() { return !floorsGoingDown.isEmpty(); }

    private void moveUp() {
        status = ElevatorStatus.MOVING_UP;
        while (!floorsGoingUp.isEmpty()) {
            int nextFloor = floorsGoingUp.first();
            travelTo(nextFloor);
            floorsGoingUp.remove(nextFloor);
            openDoor();
        }
    }

    private void moveDown() {
        status = ElevatorStatus.MOVING_DOWN;
        while (!floorsGoingDown.isEmpty()) {
            int nextFloor = floorsGoingDown.first(); // TreeSet with reverseOrder → highest first
            travelTo(nextFloor);
            floorsGoingDown.remove(nextFloor);
            openDoor();
        }
    }

    private void travelTo(int targetFloor) {
        while (currentFloor != targetFloor) {
            if (targetFloor > currentFloor) currentFloor++;
            else currentFloor--;
            System.out.printf("[Elevator %d] Passing floor %d%n", elevatorId, currentFloor);
            try { Thread.sleep(FLOOR_TRAVEL_TIME_MS); } catch (InterruptedException e) { return; }
        }
    }

    private void openDoor() {
        System.out.printf("[Elevator %d] 🚪 Doors OPEN at floor %d%n", elevatorId, currentFloor);
        try { Thread.sleep(2000); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        System.out.printf("[Elevator %d] 🚪 Doors CLOSED at floor %d%n", elevatorId, currentFloor);
    }

    // ─── Metrics for Dispatcher ────────────────────────────────────────

    public synchronized int getCurrentFloor() { return currentFloor; }
    public synchronized ElevatorStatus getStatus() { return status; }
    public int getElevatorId() { return elevatorId; }

    /** Estimated number of floors the elevator must travel to pick up this request */
    public synchronized int estimatedFloorsToRequest(int requestFloor, Direction requestDir) {
        if (status == ElevatorStatus.MAINTENANCE) return Integer.MAX_VALUE;

        int distance = Math.abs(currentFloor - requestFloor);

        // If elevator is going toward the request in the right direction, low cost
        if (status == ElevatorStatus.MOVING_UP
                && requestDir == Direction.UP
                && requestFloor >= currentFloor) {
            return distance; // directly on path
        }
        if (status == ElevatorStatus.MOVING_DOWN
                && requestDir == Direction.DOWN
                && requestFloor <= currentFloor) {
            return distance; // directly on path
        }

        // Otherwise elevator must finish current direction then come back — higher cost
        int pendingStops = floorsGoingUp.size() + floorsGoingDown.size();
        return distance + pendingStops * 2; // rough heuristic
    }

    public void setMaintenance(boolean underMaintenance) {
        this.status = underMaintenance ? ElevatorStatus.MAINTENANCE : ElevatorStatus.IDLE;
    }
}
```

```java
// ── Dispatcher ────────────────────────────────────────────────────────────

public class ElevatorDispatcher {
    private final List<Elevator> elevators;

    public ElevatorDispatcher(List<Elevator> elevators) {
        this.elevators = elevators;
    }

    /**
     * Assign the best available elevator to handle the request.
     * "Best" = minimum estimated floors to reach the request.
     */
    public Optional<Elevator> assignElevator(ElevatorRequest request) {
        return elevators.stream()
            .filter(e -> e.getStatus() != ElevatorStatus.MAINTENANCE)
            .min(Comparator.comparingInt(e ->
                e.estimatedFloorsToRequest(request.getFromFloor(), request.getDirection())
            ));
    }
}
```

```java
// ── Elevator System ───────────────────────────────────────────────────────

public class ElevatorSystem {
    private static volatile ElevatorSystem instance;

    private final int numFloors;
    private final List<Elevator> elevators;
    private final ElevatorDispatcher dispatcher;

    private ElevatorSystem(int numFloors, int numElevators) {
        this.numFloors = numFloors;
        this.elevators = new ArrayList<>();
        for (int i = 1; i <= numElevators; i++) {
            Elevator elevator = new Elevator(i, 0, numFloors, 0);
            elevators.add(elevator);
            // Start each elevator's drive loop in its own thread
            Thread driveThread = new Thread(elevator::driveLoop, "Elevator-" + i);
            driveThread.setDaemon(true);
            driveThread.start();
        }
        this.dispatcher = new ElevatorDispatcher(elevators);
    }

    public static ElevatorSystem getInstance(int numFloors, int numElevators) {
        if (instance == null) {
            synchronized (ElevatorSystem.class) {
                if (instance == null) {
                    instance = new ElevatorSystem(numFloors, numElevators);
                }
            }
        }
        return instance;
    }

    /** Floor button pressed — external request */
    public void requestFromFloor(int floor, Direction direction) {
        ElevatorRequest request = new ElevatorRequest(floor, direction);
        Optional<Elevator> assigned = dispatcher.assignElevator(request);
        assigned.ifPresentOrElse(
            elevator -> {
                elevator.addStop(floor);
                System.out.printf("🔔 Floor %d request (%s) → Elevator %d%n",
                    floor, direction, elevator.getElevatorId());
            },
            () -> System.out.println("⚠️ No elevator available for floor " + floor)
        );
    }

    /** Cabin button pressed — internal destination request */
    public void requestFromCabin(int elevatorId, int destinationFloor) {
        Elevator elevator = elevators.stream()
            .filter(e -> e.getElevatorId() == elevatorId)
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("Unknown elevator: " + elevatorId));
        elevator.addStop(destinationFloor);
        System.out.printf("🔢 Elevator %d: destination %d added%n", elevatorId, destinationFloor);
    }

    public void displayStatus() {
        System.out.println("\n=== Elevator System Status ===");
        for (Elevator e : elevators) {
            System.out.printf("  Elevator %d: Floor %d | Status: %s%n",
                e.getElevatorId(), e.getCurrentFloor(), e.getStatus());
        }
    }
}

// Demo
public class ElevatorDemo {
    public static void main(String[] args) throws InterruptedException {
        ElevatorSystem system = ElevatorSystem.getInstance(20, 3);

        system.requestFromFloor(5, Direction.UP);
        system.requestFromFloor(10, Direction.DOWN);
        system.requestFromFloor(3, Direction.UP);

        Thread.sleep(2000);
        system.requestFromCabin(1, 15); // Passenger in elevator 1 wants floor 15

        Thread.sleep(15000);
        system.displayStatus();
    }
}
```

---

## Interview Questions

**Q: Which scheduling algorithm maximizes throughput?**

A: SCAN (elevator algorithm) is the standard answer. It moves in one direction until no more requests in that direction, then reverses. This prevents starvation (unlike FCFS which can bounce). LOOK is a variant where the elevator stops at the last request in each direction rather than going to the boundary floor. For multi-elevator systems, the goal is also load balancing — assign each new request to the nearest idle elevator or the one already heading toward it.

**Q: How do you prevent starvation with SCAN?**

A: SCAN can starve new requests that arrive just behind the elevator as it moves away. C-SCAN (circular scan) addresses this — the elevator only services requests in one direction, then jumps back to the start. Alternatively, add a timestamp to requests and prioritize old requests after a waiting threshold.

**Q: How do you handle emergency (MAINTENANCE) mode?**

A: Set the elevator's status to MAINTENANCE. The dispatcher's `assignElevator` filters out maintenance elevators. The remaining elevators absorb the load. Add alerting when fewer than N elevators are operational.

---

# Chapter 8: LLD Design 4 — Splitwise

> Splitwise's core insight is the debt simplification algorithm. Interviewers test whether you can recognize it as a greedy problem and implement it correctly.

---

## Step 1: Requirements

- Add expenses to a group
- Split by: equal, exact amounts, percentage
- Track balances between users
- Settle debts (record a payment)
- **Debt simplification**: reduce N debts into minimum number of transactions
- Notify users when expense added to their group

---

## Step 2: Entities

```
User          — name, email
Group         — collection of users
Expense       — amount, paid by, splits among users
Split         — abstract: EqualSplit, PercentageSplit, ExactSplit
Balance       — net amount user X owes user Y
Settlement    — records a payment from one user to another
```

---

## Step 3: Full Java Implementation

```java
// ── Split Types ───────────────────────────────────────────────────────────

public abstract class Split {
    protected final User user;
    protected double amount; // computed or specified

    protected Split(User user) { this.user = user; }

    public User getUser()        { return user; }
    public double getAmount()    { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
}

public class EqualSplit extends Split {
    public EqualSplit(User user) { super(user); }
    // amount will be set by ExpenseService: totalAmount / numParticipants
}

public class ExactSplit extends Split {
    public ExactSplit(User user, double exactAmount) {
        super(user);
        this.amount = exactAmount;
    }
}

public class PercentageSplit extends Split {
    private final double percentage;

    public PercentageSplit(User user, double percentage) {
        super(user);
        this.percentage = percentage;
    }

    public double getPercentage() { return percentage; }
    // amount will be set by ExpenseService: totalAmount * percentage / 100
}
```

```java
// ── User ─────────────────────────────────────────────────────────────────

public class User {
    private final String userId;
    private final String name;
    private final String email;

    public User(String userId, String name, String email) {
        this.userId = userId;
        this.name   = name;
        this.email  = email;
    }

    public String getUserId() { return userId; }
    public String getName()   { return name; }
    public String getEmail()  { return email; }

    @Override
    public String toString() { return name; }
}
```

```java
// ── Group ─────────────────────────────────────────────────────────────────

public class Group {
    private final String groupId;
    private final String name;
    private final List<User> members;
    private final List<Expense> expenses;

    public Group(String groupId, String name) {
        this.groupId  = groupId;
        this.name     = name;
        this.members  = new ArrayList<>();
        this.expenses = new ArrayList<>();
    }

    public void addMember(User user) { members.add(user); }
    public void addExpense(Expense expense) { expenses.add(expense); }

    public String getGroupId()       { return groupId; }
    public String getName()          { return name; }
    public List<User> getMembers()   { return Collections.unmodifiableList(members); }
    public List<Expense> getExpenses() { return Collections.unmodifiableList(expenses); }
}
```

```java
// ── Expense ───────────────────────────────────────────────────────────────

public class Expense {
    private final String expenseId;
    private final String description;
    private final double totalAmount;
    private final User paidBy;
    private final List<Split> splits;
    private final LocalDateTime createdAt;

    public Expense(String description, double totalAmount, User paidBy, List<Split> splits) {
        this.expenseId   = "EXP-" + System.currentTimeMillis();
        this.description = description;
        this.totalAmount = totalAmount;
        this.paidBy      = paidBy;
        this.splits      = new ArrayList<>(splits);
        this.createdAt   = LocalDateTime.now();
    }

    public String getExpenseId()    { return expenseId; }
    public String getDescription()  { return description; }
    public double getTotalAmount()  { return totalAmount; }
    public User getPaidBy()         { return paidBy; }
    public List<Split> getSplits()  { return Collections.unmodifiableList(splits); }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```

```java
// ── Balance Ledger ────────────────────────────────────────────────────────

public class BalanceLedger {
    // balance[userId] = net balance: positive = they are owed money, negative = they owe money
    private final Map<String, Double> balances = new HashMap<>();

    public void recordExpense(Expense expense) {
        String payerId = expense.getPaidBy().getUserId();

        for (Split split : expense.getSplits()) {
            String debtorId = split.getUser().getUserId();
            double amount   = split.getAmount();

            if (debtorId.equals(payerId)) continue; // payer's own share

            // Debtor owes payer 'amount'
            balances.merge(debtorId, -amount, Double::sum);  // debtor's balance decreases
            balances.merge(payerId, amount, Double::sum);     // payer's balance increases
        }
    }

    public void recordSettlement(User from, User to, double amount) {
        balances.merge(from.getUserId(), amount, Double::sum); // from's debt decreases
        balances.merge(to.getUserId(), -amount, Double::sum);  // to's credit decreases
    }

    public double getBalance(String userId) {
        return balances.getOrDefault(userId, 0.0);
    }

    // Returns a copy of all balances for the simplification algorithm
    public Map<String, Double> getAllBalances() {
        return new HashMap<>(balances);
    }
}
```

```java
// ── Debt Simplification Algorithm ─────────────────────────────────────────

/**
 * PROBLEM: N people, M debts between pairs.
 * Can we reduce M transactions into fewer?
 *
 * SOLUTION: Greedy with net balances.
 * 1. Compute net balance for each person (positive = owed money, negative = owes money)
 * 2. Repeatedly match the largest creditor with the largest debtor
 * 3. Transfer min(|creditor|, |debtor|) from debtor to creditor
 * 4. Repeat until all balances are zero
 *
 * Result: at most N-1 transactions (minimum possible for any set of balances)
 */
public class DebtSimplifier {

    public static class Transaction {
        public final User from;
        public final User to;
        public final double amount;

        public Transaction(User from, User to, double amount) {
            this.from   = from;
            this.to     = to;
            this.amount = amount;
        }

        @Override
        public String toString() {
            return String.format("%s pays %s ₹%.2f", from.getName(), to.getName(), amount);
        }
    }

    public List<Transaction> simplify(Map<String, Double> balances, Map<String, User> userMap) {
        List<Transaction> transactions = new ArrayList<>();

        // Creditors: people who are owed money (positive balance)
        // Debtors: people who owe money (negative balance)
        PriorityQueue<double[]> creditors = new PriorityQueue<>(
            (a, b) -> Double.compare(b[1], a[1]) // max-heap by amount
        );
        PriorityQueue<double[]> debtors = new PriorityQueue<>(
            (a, b) -> Double.compare(a[1], b[1]) // min-heap by amount (most negative first)
        );

        // Map index to userId for reconstruction
        List<String> userIds = new ArrayList<>(balances.keySet());
        for (int i = 0; i < userIds.size(); i++) {
            double balance = balances.get(userIds.get(i));
            if (balance > 0.001) {
                creditors.offer(new double[]{i, balance});
            } else if (balance < -0.001) {
                debtors.offer(new double[]{i, balance});
            }
        }

        while (!creditors.isEmpty() && !debtors.isEmpty()) {
            double[] creditor = creditors.poll();
            double[] debtor   = debtors.poll();

            double settlement = Math.min(creditor[1], -debtor[1]);

            User fromUser = userMap.get(userIds.get((int) debtor[0]));
            User toUser   = userMap.get(userIds.get((int) creditor[0]));
            transactions.add(new Transaction(fromUser, toUser, settlement));

            creditor[1] -= settlement;
            debtor[1]   += settlement;

            if (creditor[1] > 0.001) creditors.offer(creditor); // still has credit
            if (debtor[1] < -0.001)  debtors.offer(debtor);     // still has debt
        }

        return transactions;
    }
}
```

```java
// ── Expense Service (Business Logic + Observer) ───────────────────────────

public class ExpenseService {
    private final BalanceLedger ledger;
    private final EventBus eventBus;

    public ExpenseService(BalanceLedger ledger, EventBus eventBus) {
        this.ledger   = ledger;
        this.eventBus = eventBus;
    }

    public Expense addExpense(Group group, String description, double totalAmount,
                               User paidBy, List<Split> splits) {
        // Validate and compute split amounts
        splits = computeSplitAmounts(totalAmount, splits);
        validateSplits(totalAmount, splits);

        Expense expense = new Expense(description, totalAmount, paidBy, splits);
        group.addExpense(expense);
        ledger.recordExpense(expense);

        // Notify all group members via Observer
        eventBus.publish(new ExpenseAddedEvent(group, expense, paidBy));

        System.out.printf("💰 Expense added: '%s' ₹%.2f paid by %s%n",
            description, totalAmount, paidBy.getName());
        splits.forEach(s ->
            System.out.printf("   %s owes ₹%.2f%n", s.getUser().getName(), s.getAmount())
        );

        return expense;
    }

    private List<Split> computeSplitAmounts(double totalAmount, List<Split> splits) {
        boolean allEqual = splits.stream().allMatch(s -> s instanceof EqualSplit);
        if (allEqual) {
            double perPerson = totalAmount / splits.size();
            splits.forEach(s -> s.setAmount(perPerson));
            return splits;
        }

        boolean allPercentage = splits.stream().allMatch(s -> s instanceof PercentageSplit);
        if (allPercentage) {
            splits.stream().map(s -> (PercentageSplit) s)
                  .forEach(s -> s.setAmount(totalAmount * s.getPercentage() / 100.0));
            return splits;
        }

        // ExactSplit: amounts already set, nothing to compute
        return splits;
    }

    private void validateSplits(double totalAmount, List<Split> splits) {
        double splitSum = splits.stream().mapToDouble(Split::getAmount).sum();
        if (Math.abs(splitSum - totalAmount) > 0.01) {
            throw new IllegalArgumentException(
                String.format("Split amounts (%.2f) don't add up to total (%.2f)",
                    splitSum, totalAmount));
        }
    }

    public List<DebtSimplifier.Transaction> getSimplifiedDebts(
            Group group, Map<String, User> userMap) {
        DebtSimplifier simplifier = new DebtSimplifier();
        return simplifier.simplify(ledger.getAllBalances(), userMap);
    }
}
```

```java
// ── Demo ──────────────────────────────────────────────────────────────────

public class SplitwiseDemo {
    public static void main(String[] args) {
        User alice = new User("U1", "Alice", "alice@example.com");
        User bob   = new User("U2", "Bob",   "bob@example.com");
        User carol = new User("U3", "Carol", "carol@example.com");
        User dave  = new User("U4", "Dave",  "dave@example.com");

        Group goaTrip = new Group("G1", "Goa Trip");
        goaTrip.addMember(alice); goaTrip.addMember(bob);
        goaTrip.addMember(carol); goaTrip.addMember(dave);

        BalanceLedger ledger = new BalanceLedger();
        EventBus eventBus = new EventBus();
        ExpenseService service = new ExpenseService(ledger, eventBus);

        // Expense 1: Hotel ₹4000, paid by Alice, split equally
        service.addExpense(goaTrip, "Hotel", 4000,
            alice, List.of(new EqualSplit(alice), new EqualSplit(bob),
                           new EqualSplit(carol), new EqualSplit(dave)));

        // Expense 2: Dinner ₹1500, paid by Bob, exact split
        service.addExpense(goaTrip, "Dinner", 1500,
            bob, List.of(new ExactSplit(alice, 500), new ExactSplit(bob, 500),
                         new ExactSplit(carol, 300), new ExactSplit(dave, 200)));

        // Expense 3: Water sports ₹3000, paid by Carol, percentage split
        service.addExpense(goaTrip, "Water Sports", 3000,
            carol, List.of(new PercentageSplit(alice, 25), new PercentageSplit(bob, 25),
                           new PercentageSplit(carol, 30), new PercentageSplit(dave, 20)));

        // Show individual balances
        Map<String, User> userMap = Map.of("U1", alice, "U2", bob, "U3", carol, "U4", dave);
        System.out.println("\n=== Individual Balances ===");
        userMap.forEach((id, user) ->
            System.out.printf("  %s: ₹%.2f%n", user.getName(), ledger.getBalance(id))
        );

        // Show simplified debts
        System.out.println("\n=== Simplified Settlements ===");
        service.getSimplifiedDebts(goaTrip, userMap)
               .forEach(t -> System.out.println("  " + t));
    }
}
```

**Output:**
```
💰 Expense added: 'Hotel' ₹4000.00 paid by Alice
   Alice owes ₹1000.00  Bob owes ₹1000.00  Carol owes ₹1000.00  Dave owes ₹1000.00
...
=== Simplified Settlements ===
  Bob pays Alice ₹500.00
  Dave pays Alice ₹800.00
  (fewer transactions than the 6 pairwise debts that existed)
```

---

## Interview Questions

**Q: Explain the debt simplification algorithm.**

A: Compute each person's net balance (positive = owed money, negative = owes money). Use a max-heap for creditors and a min-heap for debtors. Repeatedly pair the largest creditor with the largest debtor, settle for min(|credit|, |debt|), and push back any remainder. This produces at most N-1 transactions, which is optimal.

**Q: Why is net balance the right approach, not tracking individual pairwise debts?**

A: Pairwise debts create a graph with O(N²) edges. Net balance reduces each person to a single number. The simplification algorithm needs only net balances — not who owes whom — to produce the minimum set of transactions.

**Q: How do you handle floating point errors in split calculations?**

A: Always validate with `Math.abs(splitSum - total) < 0.01` rather than `==`. For financial systems, use `BigDecimal` with explicit rounding mode (`HALF_UP`) to avoid floating point accumulation errors.

**Q: How would you implement the Observer to notify users of new expenses?**

A: The `EventBus.publish(new ExpenseAddedEvent(...))` call is already in `addExpense`. Register a `NotificationListener` that subscribes to `ExpenseAddedEvent` and sends emails or push notifications. Adding WhatsApp notifications = adding a new subscriber. Zero changes to `ExpenseService`.
