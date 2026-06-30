# Chapter 1: OOP Design Principles Review

> "Design principles are not rules. They are tools for thinking. When you know why they exist, you know when to break them."

---

## 1.1 The SOLID Principles

SOLID is an acronym for five principles introduced by Robert C. Martin. Each one targets a specific category of design rot — the gradual degradation of code quality over time as features are added without discipline.

---

### S — Single Responsibility Principle (SRP)

**Definition:** A class should have only one reason to change.

"Reason to change" is the key phrase. If two different business requirements could force you to modify the same class, that class has too many responsibilities.

#### ❌ Violation

```java
// This class does THREE things: data storage, validation, and persistence.
// A change to the DB schema, validation rules, OR email format all touch this file.
public class User {
    private String name;
    private String email;
    private String passwordHash;

    // Responsibility 1: Business logic / validation
    public boolean isEmailValid() {
        return email != null && email.contains("@");
    }

    // Responsibility 2: Persistence — this class knows about SQL!
    public void saveToDatabase(Connection conn) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)"
        );
        stmt.setString(1, name);
        stmt.setString(2, email);
        stmt.setString(3, passwordHash);
        stmt.executeUpdate();
    }

    // Responsibility 3: Presentation
    public String toJson() {
        return "{\"name\":\"" + name + "\",\"email\":\"" + email + "\"}";
    }
}
```

**Why this hurts:** A database migration forces you to open your domain model. A front-end JSON format change forces you to open your domain model. Three reasons to change = three bugs waiting to happen.

#### ✅ Fix

```java
// Responsibility 1: Pure data model — knows nothing about DB or HTTP
public class User {
    private final String name;
    private final String email;
    private final String passwordHash;

    public User(String name, String email, String passwordHash) {
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
    }

    public String getName()         { return name; }
    public String getEmail()        { return email; }
    public String getPasswordHash() { return passwordHash; }
}

// Responsibility 2: Validation rules live here and only here
public class UserValidator {
    public void validate(User user) {
        if (user.getEmail() == null || !user.getEmail().contains("@")) {
            throw new IllegalArgumentException("Invalid email: " + user.getEmail());
        }
        if (user.getName() == null || user.getName().isBlank()) {
            throw new IllegalArgumentException("Name cannot be blank");
        }
    }
}

// Responsibility 3: Persistence lives here
public class UserRepository {
    private final DataSource dataSource;

    public UserRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public void save(User user) throws SQLException {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(
                 "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)")) {
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setString(3, user.getPasswordHash());
            stmt.executeUpdate();
        }
    }
}

// Responsibility 4: JSON serialization (or delegate to Jackson entirely)
public class UserSerializer {
    public String toJson(User user) {
        return String.format("{\"name\":\"%s\",\"email\":\"%s\"}",
            user.getName(), user.getEmail());
    }
}
```

**Result:** Changing the database schema only touches `UserRepository`. Changing validation rules only touches `UserValidator`. No class has more than one reason to change.

---

### O — Open/Closed Principle (OCP)

**Definition:** Software entities should be open for extension but closed for modification.

"Open for extension" means you can add new behavior. "Closed for modification" means you do not change existing, tested code to do it.

#### ❌ Violation

```java
// Every new payment method requires modifying this class.
// You will break existing Stripe/PayPal logic every time you add Razorpay.
public class PaymentProcessor {
    public void process(String type, double amount) {
        if (type.equals("STRIPE")) {
            System.out.println("Processing $" + amount + " via Stripe");
            // Stripe SDK calls...
        } else if (type.equals("PAYPAL")) {
            System.out.println("Processing $" + amount + " via PayPal");
            // PayPal SDK calls...
        } else if (type.equals("RAZORPAY")) {   // Added later — touched existing file
            System.out.println("Processing $" + amount + " via Razorpay");
            // Razorpay SDK calls...
        }
        // What happens when we add UPI? We modify this file again.
    }
}
```

#### ✅ Fix

```java
// The abstraction is CLOSED for modification.
public interface PaymentGateway {
    void process(double amount);
    String getName();
}

// Each implementation is a NEW class — existing classes are never touched.
public class StripeGateway implements PaymentGateway {
    @Override
    public void process(double amount) {
        System.out.println("Processing $" + amount + " via Stripe");
        // Stripe SDK calls
    }

    @Override
    public String getName() { return "STRIPE"; }
}

public class PayPalGateway implements PaymentGateway {
    @Override
    public void process(double amount) {
        System.out.println("Processing $" + amount + " via PayPal");
    }

    @Override
    public String getName() { return "PAYPAL"; }
}

// Adding Razorpay = adding a NEW FILE. Zero modification of existing code.
public class RazorpayGateway implements PaymentGateway {
    @Override
    public void process(double amount) {
        System.out.println("Processing ₹" + amount + " via Razorpay");
    }

    @Override
    public String getName() { return "RAZORPAY"; }
}

// The processor accepts any PaymentGateway — it never needs to change.
public class PaymentProcessor {
    private final PaymentGateway gateway;

    public PaymentProcessor(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public void process(double amount) {
        gateway.process(amount);
    }
}

// Usage
PaymentProcessor processor = new PaymentProcessor(new RazorpayGateway());
processor.process(1500.00);
```

---

### L — Liskov Substitution Principle (LSP)

**Definition:** If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering the correctness of the program.

In plain terms: a subclass must be usable wherever its parent class is used, without surprising the caller.

#### ❌ Violation — The Classic Rectangle/Square Problem

```java
public class Rectangle {
    protected int width;
    protected int height;

    public void setWidth(int w)  { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int area()            { return width * height; }
}

// A square IS-A rectangle mathematically, so this seems fine...
public class Square extends Rectangle {
    @Override
    public void setWidth(int w) {
        // A square must have equal sides — so we override both.
        this.width = w;
        this.height = w;  // ← silent side effect!
    }

    @Override
    public void setHeight(int h) {
        this.width = h;   // ← silent side effect!
        this.height = h;
    }
}

// This method works correctly for Rectangle but BREAKS for Square.
public void stretchAndPrint(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    // Caller expects area = 50 for any Rectangle
    System.out.println(r.area()); // Prints 100 for Square — LSP violated!
}
```

#### ✅ Fix

```java
// Use an interface that captures only the shared contract.
public interface Shape {
    int area();
}

public class Rectangle implements Shape {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public int area() { return width * height; }
}

public class Square implements Shape {
    private final int side;

    public Square(int side) {
        this.side = side;
    }

    @Override
    public int area() { return side * side; }
}

// Both shapes are substitutable for Shape without surprises.
public void printArea(Shape shape) {
    System.out.println("Area: " + shape.area());
}
```

**Rule of thumb:** If a subclass overrides a method and either weakens a precondition, strengthens a postcondition, or throws exceptions the parent doesn't, LSP is likely violated.

---

### I — Interface Segregation Principle (ISP)

**Definition:** Clients should not be forced to depend upon interfaces they do not use.

Fat interfaces force classes to implement methods they don't need, usually resulting in empty or exception-throwing stub methods.

#### ❌ Violation

```java
// One giant interface for all workers
public interface Worker {
    void work();
    void eat();
    void sleep();
    void takeBreak();
}

// A human worker implements all of these naturally.
public class HumanWorker implements Worker {
    @Override public void work()      { System.out.println("Working..."); }
    @Override public void eat()       { System.out.println("Eating..."); }
    @Override public void sleep()     { System.out.println("Sleeping..."); }
    @Override public void takeBreak() { System.out.println("Taking break..."); }
}

// A robot also works, but it doesn't eat or sleep.
// It is FORCED to implement methods that don't apply to it.
public class RobotWorker implements Worker {
    @Override public void work()      { System.out.println("Beep boop working..."); }
    @Override public void eat()       { throw new UnsupportedOperationException("Robots don't eat!"); }
    @Override public void sleep()     { throw new UnsupportedOperationException("Robots don't sleep!"); }
    @Override public void takeBreak() { /* do nothing */ }
}
```

#### ✅ Fix

```java
// Segregated interfaces — clients implement only what they need.
public interface Workable {
    void work();
}

public interface Feedable {
    void eat();
}

public interface Restable {
    void sleep();
    void takeBreak();
}

// Human implements all three
public class HumanWorker implements Workable, Feedable, Restable {
    @Override public void work()      { System.out.println("Working..."); }
    @Override public void eat()       { System.out.println("Eating..."); }
    @Override public void sleep()     { System.out.println("Sleeping..."); }
    @Override public void takeBreak() { System.out.println("Taking break..."); }
}

// Robot implements only what it actually does
public class RobotWorker implements Workable {
    @Override public void work() { System.out.println("Beep boop working..."); }
}
```

---

### D — Dependency Inversion Principle (DIP)

**Definition:**
1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

#### ❌ Violation

```java
// High-level module (OrderService) directly depends on
// a low-level detail (MySQLOrderRepository).
// Switching to PostgreSQL requires changing OrderService.
public class OrderService {
    private MySQLOrderRepository repository = new MySQLOrderRepository(); // ← hardcoded

    public void placeOrder(Order order) {
        // ... business logic ...
        repository.save(order);
    }
}

public class MySQLOrderRepository {
    public void save(Order order) {
        System.out.println("Saving to MySQL: " + order);
    }
}
```

#### ✅ Fix

```java
// The abstraction — both high and low level depend on this
public interface OrderRepository {
    void save(Order order);
    Order findById(Long id);
}

// Low-level detail implements the abstraction
public class MySQLOrderRepository implements OrderRepository {
    @Override
    public void save(Order order) { System.out.println("Saving to MySQL: " + order); }

    @Override
    public Order findById(Long id) { /* MySQL query */ return null; }
}

// Another low-level detail — can be swapped without touching OrderService
public class PostgreSQLOrderRepository implements OrderRepository {
    @Override
    public void save(Order order) { System.out.println("Saving to PostgreSQL: " + order); }

    @Override
    public Order findById(Long id) { /* PostgreSQL query */ return null; }
}

// High-level module depends ONLY on the abstraction.
// The concrete implementation is injected (Spring's @Autowired does this).
public class OrderService {
    private final OrderRepository repository; // ← depends on interface, not impl

    public OrderService(OrderRepository repository) { // ← constructor injection
        this.repository = repository;
    }

    public void placeOrder(Order order) {
        // ... business logic ...
        repository.save(order);
    }
}

// Wiring (in Spring this is done by the IoC container)
OrderRepository repo = new PostgreSQLOrderRepository();
OrderService service = new OrderService(repo); // inject any impl
```

---

## 1.2 DRY, KISS, YAGNI

These three principles are simpler than SOLID but equally important in day-to-day code quality.

### DRY — Don't Repeat Yourself

**Definition:** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

DRY is often mistaken for "no duplicate code." It's actually about no duplicate *knowledge*. Two pieces of code can look similar but represent different concepts — forcing them into one function is the wrong DRY.

#### ❌ Violation

```java
public class OrderService {
    public double calculateTax(double amount) {
        return amount * 0.18; // GST rate hardcoded
    }
}

public class InvoiceService {
    public double computeTax(double amount) {
        return amount * 0.18; // Same knowledge duplicated!
    }
}

public class CartService {
    public double getTaxAmount(double price) {
        return price * 0.18; // And again!
    }
}
// When GST changes to 0.20, you need to find and fix 3 places.
// You will miss one. It will go to production.
```

#### ✅ Fix

```java
// The knowledge of GST rate lives in exactly one place.
public final class TaxCalculator {
    private static final double GST_RATE = 0.18;

    private TaxCalculator() {}

    public static double calculateGST(double amount) {
        return amount * GST_RATE;
    }
}

// All services delegate to the single source of truth.
public class OrderService {
    public double calculateTax(double amount) {
        return TaxCalculator.calculateGST(amount);
    }
}
```

---

### KISS — Keep It Simple, Stupid

**Definition:** Most systems work best if they are kept simple rather than made complex.

Complexity is not a sign of intelligence. The most dangerous code in any codebase is the "clever" code that only the original author understands.

#### ❌ Over-engineered

```java
// This is solving a non-problem with maximum complexity.
public abstract class AbstractUserNameFormatter {
    protected abstract String preProcess(String name);
    protected abstract String postProcess(String name);

    public final String format(String name) {
        return postProcess(capitalize(preProcess(name)));
    }

    private String capitalize(String s) {
        return s.isEmpty() ? s : Character.toUpperCase(s.charAt(0)) + s.substring(1).toLowerCase();
    }
}

public class StandardUserNameFormatter extends AbstractUserNameFormatter {
    @Override protected String preProcess(String name) { return name.trim(); }
    @Override protected String postProcess(String name) { return name; }
}
```

#### ✅ KISS

```java
public class UserNameFormatter {
    public static String format(String name) {
        if (name == null || name.isBlank()) return "";
        String trimmed = name.trim();
        return Character.toUpperCase(trimmed.charAt(0)) + trimmed.substring(1).toLowerCase();
    }
}
```

**The KISS test:** Could a junior engineer understand this in 30 seconds without asking questions? If no, ask whether the complexity is truly necessary.

---

### YAGNI — You Aren't Gonna Need It

**Definition:** Do not add functionality until it is necessary.

YAGNI is a reminder that speculative generality creates dead code — code that adds complexity without value because the anticipated use case never materialized.

#### ❌ Violation

```java
// A simple notification service. The developer "anticipates" future needs.
public class NotificationService {
    // Will we ever support postal mail? No one asked for it.
    public void sendPostalMail(String address, String message) { /* TODO */ }

    // Is there a multi-currency requirement? Not yet.
    public void sendInternationalSMS(String country, String phone, String msg) { /* TODO */ }

    // Does anyone use pager notifications in 2025?
    public void sendPagerAlert(int pagerId, String msg) { /* TODO */ }

    // This is the only thing anyone actually needs right now:
    public void sendEmail(String email, String message) {
        System.out.println("Sending email to " + email + ": " + message);
    }
}
```

#### ✅ YAGNI

```java
// Build what's needed NOW. Extend when requirements actually arrive.
public class NotificationService {
    public void sendEmail(String email, String message) {
        System.out.println("Sending email to " + email + ": " + message);
    }
}
```

**When to apply YAGNI:** If you hear yourself saying "we might need this later" and there's no concrete requirement, delete it. The design patterns in this book are the *right* kind of extensibility — they respond to real, known variation points, not imagined ones.

---

## 1.3 Composition Over Inheritance

### When Inheritance Hurts You

Inheritance models an IS-A relationship. It is powerful but brittle: a subclass is tightly coupled to its parent, and changes to the parent propagate down unpredictably.

The "Fragile Base Class Problem": when you change a method in a parent class, you might break one of ten subclasses without realizing it.

#### ❌ Inheritance Gone Wrong

```java
public class Bird {
    public void fly() {
        System.out.println("Flying!");
    }

    public void eat() {
        System.out.println("Eating!");
    }
}

// Penguins ARE birds, so this seems right...
public class Penguin extends Bird {
    @Override
    public void fly() {
        // Penguins can't fly. Now we must either:
        // 1. Throw an exception (violates LSP)
        // 2. Do nothing (surprising and misleading)
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}

// Ostrich also can't fly. RubberDuck also can't fly.
// We keep piling up exceptions and overrides.
```

#### ✅ Composition

```java
// Behaviors as interfaces
public interface Flyable {
    void fly();
}

public interface Swimmable {
    void swim();
}

public interface Eatable {
    void eat();
}

// Concrete behavior implementations
public class FlyingBehavior implements Flyable {
    @Override
    public void fly() { System.out.println("Flapping wings, soaring!"); }
}

public class SwimmingBehavior implements Swimmable {
    @Override
    public void swim() { System.out.println("Swimming through water!"); }
}

// Bird HAS-A behaviors rather than IS-A everything
public class Bird {
    private final Flyable flyBehavior;
    private final Swimmable swimBehavior;

    public Bird(Flyable flyBehavior, Swimmable swimBehavior) {
        this.flyBehavior = flyBehavior;
        this.swimBehavior = swimBehavior;
    }

    public void fly()  { flyBehavior.fly(); }
    public void swim() { swimBehavior.swim(); }
}

// Eagle: can fly, can't really swim
public class Eagle extends Bird {
    public Eagle() {
        super(new FlyingBehavior(), () -> System.out.println("Eagles don't swim!"));
    }
}

// Penguin: can swim, can't fly
public class Penguin extends Bird {
    public Penguin() {
        super(() -> System.out.println("Penguins can't fly!"), new SwimmingBehavior());
    }
}
```

**Rule of thumb:** Prefer composition when:
- The behavior might vary independently of the class hierarchy
- You need to mix behaviors (a duck can BOTH fly and swim)
- You want to change behavior at runtime
- The IS-A relationship breaks for edge cases (Penguin problem)

Prefer inheritance when:
- The relationship is a genuine, stable IS-A
- The child reuses most of the parent's behavior without overriding core methods
- You are using inheritance for polymorphism through a common interface

---

## 1.4 Coupling and Cohesion

### High Cohesion

**Cohesion** measures how related the responsibilities within a single class are.

A highly cohesive class does one thing and does it well — all its methods and fields are related to a single concept.

```java
// LOW cohesion — this class is a junk drawer
public class Utilities {
    public double calculateGST(double amount) { return amount * 0.18; }
    public String formatDate(LocalDate date)  { return date.toString(); }
    public boolean isEmailValid(String email) { return email.contains("@"); }
    public void sendPushNotification(String token, String msg) { /* ... */ }
    public byte[] compressImage(byte[] imageData) { /* ... */ }
}

// HIGH cohesion — each class has a clear, singular purpose
public class TaxCalculator {
    public double calculateGST(double amount) { return amount * 0.18; }
    public double calculateIncomeTax(double amount) { /* ... */ return 0; }
}

public class EmailValidator {
    private static final Pattern EMAIL_PATTERN =
        Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");

    public boolean isValid(String email) {
        return email != null && EMAIL_PATTERN.matcher(email).matches();
    }
}
```

### Loose Coupling

**Coupling** measures how much one class knows about another.

Tightly coupled classes are hard to test, reuse, and change independently. Loose coupling means a class depends on abstractions rather than concrete implementations.

```java
// TIGHT coupling — OrderService is glued to EmailNotificationService
public class OrderService {
    private EmailNotificationService emailService = new EmailNotificationService();

    public void placeOrder(Order order) {
        // place order logic...
        emailService.sendOrderConfirmation(order.getCustomerEmail(), order); // ← direct dependency
    }
}

// LOOSE coupling — OrderService depends on an abstraction
public interface NotificationService {
    void notifyOrderPlaced(Order order);
}

public class OrderService {
    private final NotificationService notificationService; // ← depends on interface

    public OrderService(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    public void placeOrder(Order order) {
        // place order logic...
        notificationService.notifyOrderPlaced(order); // ← works for Email, SMS, Push, anything
    }
}
```

**The goal:** Each class should be a well-defined expert (high cohesion) that communicates with other experts through narrow, stable interfaces (loose coupling).

---

## 1.5 Tell Don't Ask

**Definition:** Tell an object what to do rather than asking it for data and doing the computation yourself.

"Asking" means you extract data from an object, reason about it, and act. This means the caller is doing the object's job — spreading business logic into the wrong places.

#### ❌ Ask (procedural thinking in OOP clothing)

```java
public class OrderProcessor {
    public void processOrder(Order order) {
        // ASKING the order for its state, then making decisions externally
        if (order.getStatus() == OrderStatus.PENDING
            && order.getPayment().getStatus() == PaymentStatus.CONFIRMED
            && order.getItems().size() > 0) {

            order.setStatus(OrderStatus.PROCESSING);
            // ... more logic that belongs inside Order
        }
    }
}
```

#### ✅ Tell

```java
public class Order {
    private OrderStatus status;
    private Payment payment;
    private List<OrderItem> items;

    // The knowledge of "can I be processed?" lives with the Order itself.
    public boolean canBeProcessed() {
        return status == OrderStatus.PENDING
            && payment.isConfirmed()
            && !items.isEmpty();
    }

    // Tell the order to process itself — it knows how.
    public void process() {
        if (!canBeProcessed()) {
            throw new IllegalStateException("Order cannot be processed in state: " + status);
        }
        this.status = OrderStatus.PROCESSING;
        // other internal state changes...
    }
}

public class OrderProcessor {
    public void processOrder(Order order) {
        order.process(); // ← Tell. Simple. Logic is where the data lives.
    }
}
```

**Tell Don't Ask as a design smell detector:** Every time you write `if (object.getSomething() == X)` outside the object, ask yourself: "Should this condition live *inside* the object?"

---

## Chapter 1 Summary

| Principle | One-Line Summary | Common Violation |
|-----------|-----------------|-----------------|
| SRP | One class, one reason to change | God classes / utility dumping grounds |
| OCP | Extend by adding, not modifying | Switch/if-else chains for type dispatch |
| LSP | Subclasses must not surprise callers | Exception-throwing override methods |
| ISP | Small, focused interfaces | One fat interface for all clients |
| DIP | Depend on abstractions, not concretions | `new ConcreteImpl()` inside high-level modules |
| DRY | Single source of truth | Copy-pasted business logic |
| KISS | Simple over clever | Speculative abstractions for one use case |
| YAGNI | Build what's needed now | TODO methods, unused extension points |
| Composition | Behavior as interchangeable objects | Deep inheritance hierarchies |
| High Cohesion | One thing, done well | Utility/helper catch-all classes |
| Loose Coupling | Depend on interfaces | Direct `new` calls across layers |
| Tell Don't Ask | Objects act on their own data | Getter chains in external logic |

These principles reappear in every design pattern and every LLD design in this book. When you encounter a pattern that feels arbitrary, ask: "Which principle does this enforce?" The answer always makes the pattern memorable.
