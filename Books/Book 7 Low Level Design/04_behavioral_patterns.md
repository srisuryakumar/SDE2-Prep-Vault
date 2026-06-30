# Chapter 4: Behavioral Patterns

> Behavioral patterns focus on communication between objects — how responsibilities are distributed and how objects cooperate to accomplish tasks that no single object could do alone.

---

## 4.1 Observer / Event Bus Pattern

### The Problem: Direct Coupling Between Services

```java
// ❌ BEFORE — OrderService directly calls every downstream service.
// Adding a new responder (e.g., FraudDetectionService) means modifying OrderService.
// OrderService now knows about Payment, Inventory, Notification, AND Fraud.
public class OrderService {
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    // Adding fraud detection requires changing this class ← OCP violated

    public void placeOrder(Order order) {
        // Core logic
        orderRepository.save(order);

        // Now OrderService is the coordinator for everyone
        paymentService.reserveFunds(order);
        inventoryService.decreaseStock(order);
        notificationService.sendOrderConfirmation(order);
        // Every new requirement comes back to this method
    }
}
```

### Observer Pattern: Decouple Publishers from Subscribers

```
EventBus
    ├── publish(event) → notifies all subscribers for this event type
    └── subscribe(eventType, handler) → register interest

OrderService → publishes OrderPlacedEvent
    ↑ no knowledge of who's listening
PaymentService ← subscribes to OrderPlacedEvent
InventoryService ← subscribes to OrderPlacedEvent
NotificationService ← subscribes to OrderPlacedEvent
FraudDetectionService ← subscribes to OrderPlacedEvent (added without touching OrderService)
```

```java
// The event — a plain data object describing what happened
public class OrderPlacedEvent {
    private final Long orderId;
    private final Long customerId;
    private final double totalAmount;
    private final List<OrderItem> items;
    private final Instant occurredAt;

    public OrderPlacedEvent(Long orderId, Long customerId, double totalAmount,
                             List<OrderItem> items) {
        this.orderId     = orderId;
        this.customerId  = customerId;
        this.totalAmount = totalAmount;
        this.items       = Collections.unmodifiableList(new ArrayList<>(items));
        this.occurredAt  = Instant.now();
    }

    public Long getOrderId()        { return orderId; }
    public Long getCustomerId()     { return customerId; }
    public double getTotalAmount()  { return totalAmount; }
    public List<OrderItem> getItems() { return items; }
    public Instant getOccurredAt() { return occurredAt; }
}

public class OrderCancelledEvent {
    private final Long orderId;
    private final String reason;
    public OrderCancelledEvent(Long orderId, String reason) {
        this.orderId = orderId;
        this.reason  = reason;
    }
    public Long getOrderId()   { return orderId; }
    public String getReason()  { return reason; }
}

// Generic listener interface
@FunctionalInterface
public interface EventListener<T> {
    void onEvent(T event);
}

// The EventBus — registry of listeners per event type
public class EventBus {
    // Map from event class to list of listeners for that class
    private final Map<Class<?>, List<EventListener<Object>>> listeners = new ConcurrentHashMap<>();

    @SuppressWarnings("unchecked")
    public <T> void subscribe(Class<T> eventType, EventListener<T> listener) {
        listeners
            .computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>())
            .add((EventListener<Object>) listener);
    }

    public <T> void publish(T event) {
        List<EventListener<Object>> eventListeners = listeners.get(event.getClass());
        if (eventListeners != null) {
            for (EventListener<Object> listener : eventListeners) {
                try {
                    listener.onEvent(event);
                } catch (Exception e) {
                    // One failing listener must not break others
                    System.err.println("Listener failed for event " + event.getClass().getSimpleName()
                        + ": " + e.getMessage());
                }
            }
        }
    }

    public <T> void unsubscribe(Class<T> eventType, EventListener<T> listener) {
        List<EventListener<Object>> eventListeners = listeners.get(eventType);
        if (eventListeners != null) {
            eventListeners.remove(listener);
        }
    }
}

// ✅ AFTER — OrderService only knows about orders
public class OrderService {
    private final OrderRepository orderRepository;
    private final EventBus eventBus;

    public OrderService(OrderRepository orderRepository, EventBus eventBus) {
        this.orderRepository = orderRepository;
        this.eventBus        = eventBus;
    }

    public Order placeOrder(Long customerId, List<OrderItem> items) {
        Order order = new Order(customerId, items);
        orderRepository.save(order);

        // Publish the event — OrderService has NO IDEA who listens
        eventBus.publish(new OrderPlacedEvent(
            order.getId(), customerId, order.getTotal(), items
        ));

        return order;
    }
}

// Each listener handles its own concern — independently, in its own class
public class PaymentEventListener {
    private final PaymentService paymentService;

    public PaymentEventListener(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("[Payment] Reserving ₹" + event.getTotalAmount()
            + " for order " + event.getOrderId());
        paymentService.reserveFunds(event.getOrderId(), event.getTotalAmount());
    }
}

public class InventoryEventListener {
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("[Inventory] Decreasing stock for order " + event.getOrderId());
        event.getItems().forEach(item ->
            System.out.println("  Decreasing: " + item.getProductId() + " x" + item.getQuantity())
        );
    }
}

public class NotificationEventListener {
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("[Notification] Sending confirmation to customer "
            + event.getCustomerId() + " for order " + event.getOrderId());
    }

    public void onOrderCancelled(OrderCancelledEvent event) {
        System.out.println("[Notification] Sending cancellation notice for order "
            + event.getOrderId() + " (reason: " + event.getReason() + ")");
    }
}

// Wiring
EventBus eventBus = new EventBus();

PaymentEventListener paymentListener = new PaymentEventListener(paymentService);
InventoryEventListener inventoryListener = new InventoryEventListener();
NotificationEventListener notificationListener = new NotificationEventListener();

eventBus.subscribe(OrderPlacedEvent.class, paymentListener::onOrderPlaced);
eventBus.subscribe(OrderPlacedEvent.class, inventoryListener::onOrderPlaced);
eventBus.subscribe(OrderPlacedEvent.class, notificationListener::onOrderPlaced);
eventBus.subscribe(OrderCancelledEvent.class, notificationListener::onOrderCancelled);

// Adding FraudDetection — ZERO changes to OrderService
eventBus.subscribe(OrderPlacedEvent.class, event ->
    System.out.println("[Fraud] Checking order " + event.getOrderId() + " for fraud")
);
```

### Spring's @EventListener

```java
// Spring has this built in:
@Service
public class OrderService {
    @Autowired private ApplicationEventPublisher publisher;

    public void placeOrder(Order order) {
        orderRepository.save(order);
        publisher.publishEvent(new OrderPlacedEvent(order)); // Spring handles routing
    }
}

@Component
public class InventoryListener {
    @EventListener // Spring subscribes this method automatically
    public void handleOrderPlaced(OrderPlacedEvent event) {
        // decrease stock
    }

    @EventListener
    @Async // run in a separate thread pool — non-blocking
    public void sendEmailAsync(OrderPlacedEvent event) {
        // send email asynchronously
    }
}
```

**Kafka is Observer at scale:** Producers publish to topics, consumers subscribe. Exactly the same pattern, distributed and durable.

---

## 4.2 Strategy Pattern

### The Problem: if/else Chains That Grow Forever

```java
// ❌ BEFORE — every new pricing rule requires modifying this method
public class PricingEngine {
    public double calculatePrice(Order order, String customerType) {
        double basePrice = order.getBasePrice();

        if (customerType.equals("REGULAR")) {
            return basePrice;
        } else if (customerType.equals("PREMIUM")) {
            return basePrice * 0.85;             // 15% discount
        } else if (customerType.equals("EMPLOYEE")) {
            return basePrice * 0.70;             // 30% discount
        } else if (customerType.equals("WHOLESALE")) {
            return order.getQuantity() >= 100
                ? basePrice * 0.60               // 40% for bulk
                : basePrice * 0.80;              // 20% otherwise
        }
        // Adding STUDENT or LOYALTY_MEMBER means touching this file again
        return basePrice;
    }
}
```

### Strategy Pattern: Extract Algorithms into Interchangeable Classes

```java
// The strategy interface — the "algorithm" abstraction
public interface PricingStrategy {
    double calculate(Order order);
    String getStrategyName();
}

// Concrete strategies — each encapsulates one pricing algorithm
public class RegularPricingStrategy implements PricingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getBasePrice();
    }
    @Override
    public String getStrategyName() { return "REGULAR"; }
}

public class PremiumPricingStrategy implements PricingStrategy {
    private final double discountRate;

    public PremiumPricingStrategy(double discountRate) {
        this.discountRate = discountRate;
    }

    @Override
    public double calculate(Order order) {
        return order.getBasePrice() * (1 - discountRate);
    }
    @Override
    public String getStrategyName() { return "PREMIUM (discount=" + discountRate + ")"; }
}

public class WholesalePricingStrategy implements PricingStrategy {
    private static final int BULK_THRESHOLD = 100;

    @Override
    public double calculate(Order order) {
        double discount = order.getQuantity() >= BULK_THRESHOLD ? 0.40 : 0.20;
        return order.getBasePrice() * (1 - discount);
    }
    @Override
    public String getStrategyName() { return "WHOLESALE"; }
}

public class LoyaltyPricingStrategy implements PricingStrategy {
    private final int loyaltyPoints;

    public LoyaltyPricingStrategy(int loyaltyPoints) {
        this.loyaltyPoints = loyaltyPoints;
    }

    @Override
    public double calculate(Order order) {
        // 1 loyalty point = ₹0.50 discount, max 20% discount
        double pointsDiscount = Math.min(loyaltyPoints * 0.50, order.getBasePrice() * 0.20);
        return order.getBasePrice() - pointsDiscount;
    }
    @Override
    public String getStrategyName() { return "LOYALTY (points=" + loyaltyPoints + ")"; }
}

// Context — uses whatever strategy is given to it
public class PricingEngine {
    private PricingStrategy strategy;

    public PricingEngine(PricingStrategy strategy) {
        this.strategy = strategy;
    }

    // Can also switch strategy at runtime
    public void setStrategy(PricingStrategy strategy) {
        this.strategy = strategy;
    }

    public double calculatePrice(Order order) {
        double price = strategy.calculate(order);
        System.out.printf("Strategy: %-30s Base: ₹%.2f → Price: ₹%.2f%n",
            strategy.getStrategyName(), order.getBasePrice(), price);
        return price;
    }
}

// Strategy registry — clean factory for strategy selection
public class PricingStrategyFactory {
    private final Map<String, PricingStrategy> strategies = new HashMap<>();

    public PricingStrategyFactory() {
        strategies.put("REGULAR",   new RegularPricingStrategy());
        strategies.put("PREMIUM",   new PremiumPricingStrategy(0.15));
        strategies.put("EMPLOYEE",  new PremiumPricingStrategy(0.30));
        strategies.put("WHOLESALE", new WholesalePricingStrategy());
    }

    public PricingStrategy getStrategy(String customerType) {
        PricingStrategy strategy = strategies.get(customerType.toUpperCase());
        if (strategy == null) {
            throw new IllegalArgumentException("Unknown customer type: " + customerType);
        }
        return strategy;
    }

    // Adding new strategy: strategies.put("STUDENT", new StudentPricingStrategy());
    // Zero changes to PricingEngine
    public void register(String type, PricingStrategy strategy) {
        strategies.put(type.toUpperCase(), strategy);
    }
}
```

### Cache Eviction Strategies (Another Classic)

```java
public interface EvictionPolicy<K> {
    void onAccess(K key);
    void onInsert(K key);
    K evict(); // returns the key to remove
}

public class LRUEvictionPolicy<K> implements EvictionPolicy<K> {
    private final LinkedHashMap<K, Boolean> accessOrder;

    public LRUEvictionPolicy(int capacity) {
        // accessOrder=true → LinkedHashMap orders by access time (LRU-ready)
        this.accessOrder = new LinkedHashMap<>(capacity, 0.75f, true);
    }

    @Override
    public void onAccess(K key) { accessOrder.get(key); } // moves to end

    @Override
    public void onInsert(K key) { accessOrder.put(key, true); }

    @Override
    public K evict() {
        K lruKey = accessOrder.entrySet().iterator().next().getKey(); // head = LRU
        accessOrder.remove(lruKey);
        return lruKey;
    }
}

public class LFUEvictionPolicy<K> implements EvictionPolicy<K> {
    private final Map<K, Integer> frequency = new HashMap<>();

    @Override
    public void onAccess(K key) { frequency.merge(key, 1, Integer::sum); }

    @Override
    public void onInsert(K key) { frequency.put(key, 1); }

    @Override
    public K evict() {
        return frequency.entrySet().stream()
            .min(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey)
            .orElseThrow(() -> new IllegalStateException("Cache is empty"));
    }
}
```

---

## 4.3 Command Pattern

### Intent: Encapsulate a Request as an Object

This enables:
- **Undo/Redo**: store a history of commands, call `undo()` in reverse
- **Queuing**: send commands to a work queue to execute later
- **Logging**: persist commands for audit trails or replay

```java
// The command interface
public interface Command {
    void execute();
    void undo();
    String getDescription();
}

// Receiver — the object that actually does the work
public class TextDocument {
    private final StringBuilder content = new StringBuilder();

    public void insertText(int position, String text) {
        content.insert(position, text);
    }

    public void deleteText(int position, int length) {
        content.delete(position, position + length);
    }

    public String getContent() { return content.toString(); }
}

// Concrete Commands
public class InsertTextCommand implements Command {
    private final TextDocument document;
    private final int position;
    private final String text;

    public InsertTextCommand(TextDocument document, int position, String text) {
        this.document = document;
        this.position = position;
        this.text     = text;
    }

    @Override
    public void execute() {
        document.insertText(position, text);
    }

    @Override
    public void undo() {
        // Reverse: delete what was inserted
        document.deleteText(position, text.length());
    }

    @Override
    public String getDescription() {
        return String.format("Insert '%s' at position %d", text, position);
    }
}

public class DeleteTextCommand implements Command {
    private final TextDocument document;
    private final int position;
    private final int length;
    private String deletedText; // saved during execute for undo

    public DeleteTextCommand(TextDocument document, int position, int length) {
        this.document = document;
        this.position = position;
        this.length   = length;
    }

    @Override
    public void execute() {
        String content = document.getContent();
        deletedText = content.substring(position, position + length);
        document.deleteText(position, length);
    }

    @Override
    public void undo() {
        // Reverse: re-insert what was deleted
        document.insertText(position, deletedText);
    }

    @Override
    public String getDescription() {
        return String.format("Delete %d chars at position %d", length, position);
    }
}

// Invoker — manages command history, provides undo/redo
public class TextEditor {
    private final TextDocument document;
    private final Deque<Command> undoStack = new ArrayDeque<>();
    private final Deque<Command> redoStack = new ArrayDeque<>();

    public TextEditor() {
        this.document = new TextDocument();
    }

    public void execute(Command command) {
        command.execute();
        undoStack.push(command);
        redoStack.clear(); // new command clears redo history
        System.out.println("Executed: " + command.getDescription());
        System.out.println("Content: \"" + document.getContent() + "\"");
    }

    public void undo() {
        if (undoStack.isEmpty()) {
            System.out.println("Nothing to undo");
            return;
        }
        Command command = undoStack.pop();
        command.undo();
        redoStack.push(command);
        System.out.println("Undid: " + command.getDescription());
        System.out.println("Content: \"" + document.getContent() + "\"");
    }

    public void redo() {
        if (redoStack.isEmpty()) {
            System.out.println("Nothing to redo");
            return;
        }
        Command command = redoStack.pop();
        command.execute();
        undoStack.push(command);
        System.out.println("Redid: " + command.getDescription());
        System.out.println("Content: \"" + document.getContent() + "\"");
    }
}

// Usage
TextEditor editor = new TextEditor();
editor.execute(new InsertTextCommand(editor.document, 0, "Hello"));
// Content: "Hello"
editor.execute(new InsertTextCommand(editor.document, 5, " World"));
// Content: "Hello World"
editor.execute(new DeleteTextCommand(editor.document, 5, 6));
// Content: "Hello"
editor.undo();  // Undid delete → Content: "Hello World"
editor.undo();  // Undid insert " World" → Content: "Hello"
editor.redo();  // Redid insert " World" → Content: "Hello World"
```

---

## 4.4 State Pattern

### The Problem: if/else Hell for State-Dependent Behavior

```java
// ❌ BEFORE — Vending machine with explicit state checks everywhere
public class VendingMachine {
    private enum State { IDLE, MONEY_INSERTED, DISPENSING, OUT_OF_STOCK }
    private State state = State.IDLE;
    private int stock = 10;
    private double insertedMoney = 0;

    public void insertMoney(double amount) {
        if (state == State.IDLE) {
            insertedMoney += amount;
            state = State.MONEY_INSERTED;
        } else if (state == State.MONEY_INSERTED) {
            insertedMoney += amount;  // can add more
        } else if (state == State.OUT_OF_STOCK) {
            System.out.println("Out of stock, cannot insert money");
        } else {
            System.out.println("Cannot insert money now");
        }
        // Adding a new state (e.g., MAINTENANCE) requires touching every method
    }

    public void selectProduct() {
        if (state == State.MONEY_INSERTED && insertedMoney >= 20) {
            if (stock > 0) {
                state = State.DISPENSING;
                dispense();
            } else {
                state = State.OUT_OF_STOCK;
            }
        } else if (state == State.IDLE) {
            System.out.println("Please insert money first");
        }
        // ... more conditions
    }
}
```

### State Pattern: Each State Handles Its Own Behavior

```
VendingMachine (context)
    └── current state → delegates all actions to it

VendingMachineState (interface)
    ├── IdleState
    ├── MoneyInsertedState
    ├── DispensingState
    └── OutOfStockState
```

```java
// State interface — every state handles the same set of actions
public interface VendingMachineState {
    void insertMoney(VendingMachine machine, double amount);
    void selectProduct(VendingMachine machine);
    void dispenseProduct(VendingMachine machine);
    void cancelTransaction(VendingMachine machine);
    String getStateName();
}

// Concrete States
public class IdleState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.printf("Inserted ₹%.2f. Total: ₹%.2f%n", amount, machine.getInsertedMoney());
        machine.setState(new MoneyInsertedState());
    }

    @Override
    public void selectProduct(VendingMachine machine) {
        System.out.println("[Idle] Please insert money before selecting a product.");
    }

    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("[Idle] No product selected.");
    }

    @Override
    public void cancelTransaction(VendingMachine machine) {
        System.out.println("[Idle] Nothing to cancel.");
    }

    @Override
    public String getStateName() { return "IDLE"; }
}

public class MoneyInsertedState implements VendingMachineState {
    private static final double PRODUCT_PRICE = 20.0;

    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.printf("Added ₹%.2f. Total: ₹%.2f%n", amount, machine.getInsertedMoney());
    }

    @Override
    public void selectProduct(VendingMachine machine) {
        if (machine.getInsertedMoney() < PRODUCT_PRICE) {
            System.out.printf("[MoneyInserted] Need ₹%.2f more. Have ₹%.2f.%n",
                PRODUCT_PRICE - machine.getInsertedMoney(), machine.getInsertedMoney());
            return;
        }
        if (machine.getStock() == 0) {
            System.out.println("[MoneyInserted] Out of stock. Returning money.");
            machine.returnMoney();
            machine.setState(new OutOfStockState());
            return;
        }
        System.out.println("[MoneyInserted] Product selected. Dispensing...");
        machine.setState(new DispensingState());
        machine.dispense();
    }

    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("[MoneyInserted] Select a product first.");
    }

    @Override
    public void cancelTransaction(VendingMachine machine) {
        System.out.printf("[MoneyInserted] Transaction cancelled. Returning ₹%.2f.%n",
            machine.getInsertedMoney());
        machine.returnMoney();
        machine.setState(new IdleState());
    }

    @Override
    public String getStateName() { return "MONEY_INSERTED"; }
}

public class DispensingState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        System.out.println("[Dispensing] Please wait, dispensing in progress.");
    }

    @Override
    public void selectProduct(VendingMachine machine) {
        System.out.println("[Dispensing] Already dispensing.");
    }

    @Override
    public void dispenseProduct(VendingMachine machine) {
        machine.decreaseStock();
        double change = machine.getInsertedMoney() - 20.0;
        if (change > 0) {
            System.out.printf("[Dispensing] Returning change: ₹%.2f%n", change);
        }
        machine.clearMoney();
        System.out.println("[Dispensing] Product dispensed! Enjoy.");
        if (machine.getStock() == 0) {
            machine.setState(new OutOfStockState());
        } else {
            machine.setState(new IdleState());
        }
    }

    @Override
    public void cancelTransaction(VendingMachine machine) {
        System.out.println("[Dispensing] Cannot cancel, dispensing in progress.");
    }

    @Override
    public String getStateName() { return "DISPENSING"; }
}

public class OutOfStockState implements VendingMachineState {
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        System.out.println("[OutOfStock] Machine is out of stock. Cannot accept money.");
    }

    @Override
    public void selectProduct(VendingMachine machine) {
        System.out.println("[OutOfStock] Machine is out of stock.");
    }

    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("[OutOfStock] No products to dispense.");
    }

    @Override
    public void cancelTransaction(VendingMachine machine) {
        System.out.println("[OutOfStock] No active transaction.");
    }

    @Override
    public String getStateName() { return "OUT_OF_STOCK"; }
}

// Context — delegates all behavior to the current state
public class VendingMachine {
    private VendingMachineState currentState;
    private int stock;
    private double insertedMoney;

    public VendingMachine(int initialStock) {
        this.stock         = initialStock;
        this.insertedMoney = 0;
        this.currentState  = stock > 0 ? new IdleState() : new OutOfStockState();
    }

    // Delegation to current state
    public void insertMoney(double amount)   { currentState.insertMoney(this, amount); }
    public void selectProduct()              { currentState.selectProduct(this); }
    public void dispense()                   { currentState.dispenseProduct(this); }
    public void cancelTransaction()          { currentState.cancelTransaction(this); }

    // State transitions — called by states themselves
    public void setState(VendingMachineState state) {
        System.out.println("[State] " + currentState.getStateName() + " → " + state.getStateName());
        this.currentState = state;
    }

    // Internal state mutators — only states should call these
    public void addMoney(double amount)   { this.insertedMoney += amount; }
    public void clearMoney()              { this.insertedMoney = 0; }
    public void returnMoney()             { System.out.printf("Returned ₹%.2f%n", insertedMoney); clearMoney(); }
    public void decreaseStock()           { this.stock--; }

    public double getInsertedMoney()      { return insertedMoney; }
    public int getStock()                 { return stock; }
    public String getCurrentStateName()   { return currentState.getStateName(); }
}

// Usage
VendingMachine machine = new VendingMachine(2);
machine.selectProduct();          // [Idle] Please insert money first.
machine.insertMoney(10.0);        // Inserted ₹10. Total: ₹10
machine.insertMoney(15.0);        // Added ₹15. Total: ₹25
machine.selectProduct();          // Dispenses product, returns ₹5 change
machine.insertMoney(20.0);        // Second product
machine.selectProduct();          // Dispenses last product → transitions to OUT_OF_STOCK
machine.insertMoney(20.0);        // [OutOfStock] Cannot accept money
```

---

## 4.5 Template Method Pattern

### Intent: Define Algorithm Skeleton, Defer Steps to Subclasses

```java
// Abstract class defining the algorithm skeleton
public abstract class DataExporter {
    // TEMPLATE METHOD — final so subclasses can't reorder steps
    public final void export(String destination) {
        List<Map<String, Object>> rawData = fetchData();
        List<Map<String, Object>> processed = processData(rawData);
        String formatted = formatData(processed);
        writeOutput(formatted, destination);
        sendNotification(destination); // hook — has default implementation
    }

    // Abstract steps — subclasses MUST implement
    protected abstract List<Map<String, Object>> fetchData();
    protected abstract String formatData(List<Map<String, Object>> data);

    // Concrete step — shared by all subclasses
    protected List<Map<String, Object>> processData(List<Map<String, Object>> data) {
        // Default: filter out nulls, sort by "name"
        return data.stream()
            .filter(row -> row.get("id") != null)
            .sorted(Comparator.comparing(row -> String.valueOf(row.get("name"))))
            .collect(java.util.stream.Collectors.toList());
    }

    // Hook — subclasses MAY override (optional customization point)
    protected void sendNotification(String destination) {
        System.out.println("Export complete: " + destination);
    }

    private void writeOutput(String content, String destination) {
        System.out.printf("Writing %d chars to %s%n", content.length(), destination);
        // actual file write
    }
}

// Concrete subclass — provides CSV-specific steps
public class CsvDataExporter extends DataExporter {
    private final DataSource dataSource;

    public CsvDataExporter(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    protected List<Map<String, Object>> fetchData() {
        System.out.println("Fetching data from database for CSV export...");
        return List.of(
            Map.of("id", 1, "name", "Alice", "email", "alice@example.com"),
            Map.of("id", 2, "name", "Bob",   "email", "bob@example.com")
        );
    }

    @Override
    protected String formatData(List<Map<String, Object>> data) {
        StringBuilder csv = new StringBuilder("id,name,email\n");
        data.forEach(row ->
            csv.append(row.get("id")).append(",")
               .append(row.get("name")).append(",")
               .append(row.get("email")).append("\n")
        );
        return csv.toString();
    }
}

// Concrete subclass — provides JSON-specific steps
public class JsonDataExporter extends DataExporter {
    @Override
    protected List<Map<String, Object>> fetchData() {
        System.out.println("Fetching data from API for JSON export...");
        return List.of(
            Map.of("id", 1, "name", "Alice"),
            Map.of("id", 2, "name", "Bob")
        );
    }

    @Override
    protected String formatData(List<Map<String, Object>> data) {
        // Simplified JSON serialization
        StringBuilder json = new StringBuilder("[");
        data.forEach(row ->
            json.append("{\"id\":").append(row.get("id"))
                .append(",\"name\":\"").append(row.get("name")).append("\"},")
        );
        if (json.charAt(json.length() - 1) == ',') json.deleteCharAt(json.length() - 1);
        return json.append("]").toString();
    }

    @Override
    protected void sendNotification(String destination) {
        // Override hook for JSON exporter — send webhook instead of print
        System.out.println("Webhook sent: JSON export complete at " + destination);
    }
}

// Spring's JdbcTemplate is a template method:
// It handles connection acquisition, statement preparation, exception translation,
// and connection cleanup — you provide only the SQL and the row mapping.
```

---

## 4.6 Chain of Responsibility

```java
// ════════════════════════════════════════════════════════════════════════════
// CHAIN OF RESPONSIBILITY PATTERN
// ════════════════════════════════════════════════════════════════════════════

// ── BEFORE: The problem this pattern solves ──────────────────────────────────
//
// Without Chain of Responsibility: one giant method with nested if-else.
// Every new support tier requires modifying this class — violates Open/Closed.
// The method grows indefinitely. Testing individual levels is impossible.

public class SupportSystem_BEFORE {

    // This method handles ALL support levels — a god method
    public String handleTicket(SupportTicket ticket) {
        if (ticket.getPriority() == Priority.LOW) {
            if (canLevel1Handle(ticket)) {
                return "Level 1 resolved: " + ticket.getDescription();
            } else if (ticket.getPriority() == Priority.MEDIUM) {
                if (canLevel2Handle(ticket)) {
                    return "Level 2 resolved: " + ticket.getDescription();
                } else if (ticket.getPriority() == Priority.HIGH) {
                    if (canLevel3Handle(ticket)) {
                        return "Level 3 resolved: " + ticket.getDescription();
                    } else {
                        // What if we add Priority.CRITICAL? Modify this method.
                        // What if we add Level 4? Modify this method.
                        // This class grows every time business requirements change.
                        return "Escalated to management";
                    }
                } else {
                    return "Level 2 resolved";
                }
            } else {
                return "Level 1 resolved";
            }
        }
        // This code is deeply nested, fragile, hard to test, and impossible
        // to maintain as business rules change. It violates:
        // - Single Responsibility (handles ALL levels)
        // - Open/Closed (must be modified to add new levels)
        // - Testability (cannot test Level 2 without simulating Level 1 failure)
        return "Unhandled";
    }

    private boolean canLevel1Handle(SupportTicket t) { return t.getPriority() == Priority.LOW; }
    private boolean canLevel2Handle(SupportTicket t) { return t.getPriority() == Priority.MEDIUM; }
    private boolean canLevel3Handle(SupportTicket t) { return true; }
}
```

// ── AFTER: Chain of Responsibility ───────────────────────────────────────────
//
// Each handler knows only about its own responsibility and its successor.
// Adding a new handler = new class, zero changes to existing handlers.

```java
// Handler interface
public abstract class SupportHandler {
    protected SupportHandler next;

    public SupportHandler setNext(SupportHandler next) {
        this.next = next;
        return next; // enables chaining: l1.setNext(l2).setNext(l3)
    }

    public abstract void handle(SupportTicket ticket);

    protected void passToNext(SupportTicket ticket) {
        if (next != null) {
            next.handle(ticket);
        } else {
            System.out.println("[UNRESOLVED] Ticket #" + ticket.getId()
                + " could not be resolved: " + ticket.getTitle());
        }
    }
}

public class SupportTicket {
    private final int id;
    private final String title;
    private final int severity; // 1=low, 2=medium, 3=high, 4=critical
    private final String type;  // "BILLING", "TECHNICAL", "ACCOUNT"

    public SupportTicket(int id, String title, int severity, String type) {
        this.id = id; this.title = title; this.severity = severity; this.type = type;
    }
    public int getId()        { return id; }
    public String getTitle()  { return title; }
    public int getSeverity()  { return severity; }
    public String getType()   { return type; }
}

// Concrete handlers — each handles what it can, passes the rest
public class L1SupportHandler extends SupportHandler {
    @Override
    public void handle(SupportTicket ticket) {
        if (ticket.getSeverity() == 1) {
            System.out.printf("[L1] Resolved ticket #%d: %s (FAQ/knowledge base)%n",
                ticket.getId(), ticket.getTitle());
        } else {
            System.out.printf("[L1] Ticket #%d exceeds L1 capability, escalating...%n",
                ticket.getId());
            passToNext(ticket);
        }
    }
}

public class L2SupportHandler extends SupportHandler {
    @Override
    public void handle(SupportTicket ticket) {
        if (ticket.getSeverity() <= 2) {
            System.out.printf("[L2] Resolved ticket #%d: %s (technical support)%n",
                ticket.getId(), ticket.getTitle());
        } else {
            System.out.printf("[L2] Ticket #%d too complex, escalating to L3...%n",
                ticket.getId());
            passToNext(ticket);
        }
    }
}

public class BillingHandler extends SupportHandler {
    @Override
    public void handle(SupportTicket ticket) {
        if ("BILLING".equals(ticket.getType())) {
            System.out.printf("[Billing] Resolved ticket #%d: %s%n",
                ticket.getId(), ticket.getTitle());
        } else {
            passToNext(ticket);
        }
    }
}

public class L3SupportHandler extends SupportHandler {
    @Override
    public void handle(SupportTicket ticket) {
        // L3 handles everything that reaches it
        System.out.printf("[L3 SENIOR] Resolving critical ticket #%d: %s%n",
            ticket.getId(), ticket.getTitle());
    }
}

// Wiring the chain
SupportHandler l1      = new L1SupportHandler();
SupportHandler billing = new BillingHandler();
SupportHandler l2      = new L2SupportHandler();
SupportHandler l3      = new L3SupportHandler();

l1.setNext(billing).setNext(l2).setNext(l3);

// Usage
l1.handle(new SupportTicket(1, "Can't find FAQ", 1, "GENERAL"));
// [L1] Resolved ticket #1

l1.handle(new SupportTicket(2, "Wrong charge on invoice", 2, "BILLING"));
// [L1] Escalating → [Billing] Resolved ticket #2

l1.handle(new SupportTicket(3, "Database corruption", 3, "TECHNICAL"));
// [L1] Escalating → [Billing] Pass → [L2] Escalating → [L3] Resolving
```

---

## 4.7 Iterator Pattern

### Intent: Traverse Without Exposing Internal Structure

```java
// ════════════════════════════════════════════════════════════════════════════
// ITERATOR PATTERN — BEFORE Code
// ════════════════════════════════════════════════════════════════════════════

// ── BEFORE: Exposing internal implementation ──────────────────────────────────
//
// Without Iterator, clients must know the internal structure to traverse.
// If you change from ArrayList to TreeSet, ALL client code breaks.
// The collection is tightly coupled to its traversal mechanism.

public class OrderCollection_BEFORE {
    // Internal implementation is exposed — clients see it's an ArrayList
    private ArrayList<Order> orders = new ArrayList<>();

    public void add(Order order) { orders.add(order); }

    // Client must know it's an ArrayList to iterate:
    public ArrayList<Order> getOrders() { return orders; }
}

// Client code — tightly coupled to ArrayList:
OrderCollection_BEFORE collection = new OrderCollection_BEFORE();
ArrayList<Order> orders = collection.getOrders();

// Client iterates using ArrayList's index-based access:
for (int i = 0; i < orders.size(); i++) {
    processOrder(orders.get(i));  // works only for ArrayList, not Set, not Queue
}

// Problem: if OrderCollection_BEFORE changes to TreeSet internally:
// 1. The return type must change from ArrayList to TreeSet
// 2. The client code breaks (TreeSet has no .get(i) method)
// 3. Every client that calls getOrders() must be updated
```

// ── AFTER: Iterator pattern — hide the internal structure ─────────────────────

```java
// Java's Iterator is built on this pattern
public interface Iterator<T> {
    boolean hasNext();
    T next();
}

// A custom collection — a circular buffer
public class CircularBuffer<T> {
    private final Object[] elements;
    private int head = 0;
    private int tail = 0;
    private int size = 0;
    private final int capacity;

    public CircularBuffer(int capacity) {
        this.capacity = capacity;
        this.elements = new Object[capacity];
    }

    public void add(T element) {
        if (size == capacity) throw new IllegalStateException("Buffer full");
        elements[tail] = element;
        tail = (tail + 1) % capacity;
        size++;
    }

    public T remove() {
        if (size == 0) throw new NoSuchElementException("Buffer empty");
        @SuppressWarnings("unchecked") T element = (T) elements[head];
        head = (head + 1) % capacity;
        size--;
        return element;
    }

    public int size() { return size; }

    // Returns an iterator without exposing the array structure
    public Iterator<T> iterator() {
        return new CircularBufferIterator();
    }

    private class CircularBufferIterator implements Iterator<T> {
        private int current = head;
        private int remaining = size;

        @Override
        public boolean hasNext() { return remaining > 0; }

        @Override
        @SuppressWarnings("unchecked")
        public T next() {
            if (!hasNext()) throw new NoSuchElementException();
            T element = (T) elements[current];
            current = (current + 1) % capacity;
            remaining--;
            return element;
        }
    }
}

// Usage — caller never knows about head/tail indices
CircularBuffer<String> buffer = new CircularBuffer<>(5);
buffer.add("A"); buffer.add("B"); buffer.add("C");
Iterator<String> it = buffer.iterator();
while (it.hasNext()) {
    System.out.println(it.next()); // A, B, C
}
```

---

## Chapter 4 Summary

| Pattern | When to Use | Key Mechanism |
|---------|-------------|---------------|
| Observer | Multiple parties need to react to the same event | Publisher publishes; subscribers react |
| Strategy | Multiple algorithms for same task, need to swap | Interface per algorithm, inject at runtime |
| Command | Need undo/redo, queueing, or audit log | Encapsulate request as object |
| State | Object behavior changes based on internal state | Delegate to current state object |
| Template Method | Algorithm skeleton fixed, steps vary | Abstract base class with hook methods |
| Chain of Responsibility | Request processed by one of many handlers | Pass through chain until handled |
| Iterator | Traverse collection without coupling to structure | Standard `hasNext()/next()` interface |

### Interview Questions on Behavioral Patterns

**Q: Strategy vs. State — when do you choose each?**
A: Strategy: the algorithm is chosen by the *client* at construction or call time; the object itself is stateless about which strategy to use. State: the object transitions between states *itself* based on what happens; the "strategy" switches autonomously (the vending machine changes its own state, the client doesn't pick it).

**Q: What's the difference between Observer and Event Bus?**
A: Observer (classic GoF): observers register directly with the subject and know each other's interface. Event Bus: publishers and subscribers are completely decoupled — neither knows the other exists. Event Bus is Observer at scale.

**Q: Where is Chain of Responsibility used in real systems?**
A: HTTP filter chains (Servlet filters, Spring's `FilterChain`), middleware pipelines, log level routing (DEBUG → INFO → WARN), authentication middleware (auth check → rate limit → CORS).

**Q: How does Command Pattern differ from Strategy?**
A: Strategy defines *how* to do something (algorithm). Command defines *what* to do (a specific operation on a specific receiver), captures all the information needed to invoke it later, and supports undo.
