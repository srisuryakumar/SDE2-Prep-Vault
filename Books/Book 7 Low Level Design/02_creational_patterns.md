# Chapter 2: Creational Patterns

> Creational patterns abstract the instantiation process. They give you control over *how*, *when*, and *how many* objects are created.

---

## 2.1 Singleton Pattern

### The Problem: Uncontrolled Instance Creation

Imagine your application creates a new database connection pool every time a class needs one. At scale, you'd have hundreds of connection pools, each consuming file descriptors and memory. You need exactly one instance — shared, configured once, globally accessible.

Similar cases:
- Configuration manager (reads application.properties once, serves everywhere)
- Logger (one log file, one writer)
- Cache manager (one cache, shared across the application)
- Thread pool (one pool, not fifty)

---

### Approach 1: Naive Singleton (Not Thread-Safe)

```java
// ❌ NAIVE — Works in single-threaded scenarios only.
// In a multi-threaded environment, two threads can both pass the null check
// simultaneously and create two separate instances.
public class ConfigManager {
    private static ConfigManager instance; // no volatile!
    private final Map<String, String> properties = new HashMap<>();

    private ConfigManager() {
        // Load properties from file — expensive operation
        properties.put("db.host", "localhost");
        properties.put("db.port", "5432");
        System.out.println("ConfigManager initialized");
    }

    public static ConfigManager getInstance() {
        if (instance == null) {              // Thread A and Thread B both see null here
            instance = new ConfigManager();   // Both create a new instance!
        }
        return instance;
    }

    public String get(String key) {
        return properties.getOrDefault(key, "");
    }
}
```

**Race condition:** Thread A and Thread B both reach `if (instance == null)` simultaneously before either has completed the constructor. Both create a `ConfigManager`. Now you have two instances, each with their own state.

---

### Approach 2: Synchronized Method (Thread-Safe but Slow)

```java
// ✅ Thread-safe, but every call to getInstance() acquires the lock.
// After the first initialization, synchronization is unnecessary overhead.
public class ConfigManager {
    private static ConfigManager instance;
    private final Map<String, String> properties = new HashMap<>();

    private ConfigManager() {
        properties.put("db.host", "localhost");
        properties.put("db.port", "5432");
    }

    // synchronized makes the entire method a critical section
    public static synchronized ConfigManager getInstance() {
        if (instance == null) {
            instance = new ConfigManager();
        }
        return instance;
    }
}
```

**Problem:** `synchronized` acquires a lock on every call to `getInstance()`, even after the instance exists. In a high-throughput system, this is significant contention.

---

### Approach 3: Double-Checked Locking with volatile (Production-Grade)

```java
// ✅ Thread-safe AND efficient.
// The volatile keyword ensures that writes to 'instance' are visible across all threads
// and prevents instruction reordering during construction.
public class ConfigManager {
    // volatile is CRITICAL here. Without it, a thread might see a partially
    // constructed object due to JVM instruction reordering.
    private static volatile ConfigManager instance;

    private final Map<String, String> properties = new HashMap<>();

    private ConfigManager() {
        properties.put("db.host", "localhost");
        properties.put("db.port", "5432");
        properties.put("db.name", "orders");
        System.out.println("ConfigManager initialized once.");
    }

    public static ConfigManager getInstance() {
        if (instance == null) {                 // First check (no lock needed)
            synchronized (ConfigManager.class) { // Lock only if instance might be null
                if (instance == null) {          // Second check (inside lock)
                    instance = new ConfigManager();
                }
            }
        }
        return instance;
    }

    public String get(String key) {
        return properties.getOrDefault(key, "");
    }

    public String getOrDefault(String key, String defaultValue) {
        return properties.getOrDefault(key, defaultValue);
    }
}
```

**Why volatile prevents the bug:** Without `volatile`, the JVM can reorder the three steps of `instance = new ConfigManager()`:
1. Allocate memory
2. Initialize the object
3. Assign to `instance`

A thread might see step 3 done before step 2, receiving a reference to an incompletely initialized object. `volatile` prevents this reordering.

**Why double-check:** The first `if (instance == null)` avoids locking every time. The second check inside `synchronized` ensures only one thread initializes when both first-check threads enter the synchronized block.

---

### Approach 4: Enum Singleton (The Best Java Singleton)

```java
// ✅✅ BEST APPROACH for most cases.
// The JVM guarantees a single instance per enum constant.
// Thread-safe by the JVM spec.
// Immune to reflection attacks (you can't call constructors on enum).
// Immune to serialization attacks (enum deserialization always returns the same instance).
public enum ConfigManager {
    INSTANCE;

    private final Map<String, String> properties = new HashMap<>();

    // The constructor runs exactly once, guaranteed by the JVM.
    ConfigManager() {
        properties.put("db.host", "localhost");
        properties.put("db.port", "5432");
        properties.put("db.name", "orders");
        System.out.println("ConfigManager (enum) initialized once.");
    }

    public String get(String key) {
        return properties.getOrDefault(key, "");
    }

    public String getOrDefault(String key, String defaultValue) {
        return properties.getOrDefault(key, defaultValue);
    }
}

// Usage
String host = ConfigManager.INSTANCE.get("db.host"); // "localhost"
```

**Why enum beats double-checked locking:**
- No boilerplate
- JVM guarantees thread safety
- Reflection attacks: `Constructor.newInstance()` fails on enums with `IllegalArgumentException`
- Serialization: if `ConfigManager` implements `Serializable`, DCL breaks because `readObject()` creates a new instance. Enum is immune.

**When NOT to use enum singleton:**
- When you need lazy initialization (enum initializes at class load)
- When you need to extend a class (enums cannot extend other classes)
- When you need to implement multiple interfaces (enum can implement, but it's awkward)

---

### Singleton in Spring Boot

```java
// In Spring, beans are singletons by default — you don't need to implement the pattern.
@Service
public class ConfigService {
    // Spring creates exactly one instance and injects it everywhere.
    // This IS the singleton pattern without any of the boilerplate.

    @Value("${db.host}")
    private String dbHost;

    public String getDbHost() { return dbHost; }
}

// Every @Autowired of ConfigService gets the SAME instance.
@RestController
public class OrderController {
    @Autowired
    private ConfigService configService; // Same instance as the one in PaymentController
}
```

---

## 2.2 Factory Method Pattern

### The Problem: new() Scattered Everywhere

```java
// ❌ BEFORE — Direct instantiation throughout the codebase.
// Adding Razorpay means finding every place that creates a processor and adding an else-if.
public class PaymentController {
    public void processPayment(String type, double amount) {
        if (type.equals("STRIPE")) {
            StripeProcessor processor = new StripeProcessor(); // hardcoded
            processor.charge(amount);
        } else if (type.equals("PAYPAL")) {
            PayPalProcessor processor = new PayPalProcessor();  // hardcoded
            processor.charge(amount);
        }
        // Razorpay? You touch this file. And every other file that creates processors.
    }
}
```

**Problems:**
1. OCP violated: adding a payment type requires modifying existing code
2. Knowledge of concrete classes spreads across the codebase
3. No single place to add cross-cutting concerns (logging, validation) to creation

---

### Factory Method: The Solution

The Factory Method pattern defines an interface for creating an object but lets **subclasses** decide which class to instantiate. The factory method defers instantiation to subclasses.

```
PaymentGateway (interface)
    ├── StripeGateway
    ├── PayPalGateway
    └── RazorpayGateway

PaymentGatewayFactory (abstract)
    ├── StripeFactory
    ├── PayPalFactory
    └── RazorpayFactory
```

```java
// The product interface
public interface PaymentGateway {
    void processPayment(double amount);
    void refund(double amount, String transactionId);
    String getGatewayName();
}

// Concrete products
public class StripeGateway implements PaymentGateway {
    private final String apiKey;

    public StripeGateway(String apiKey) {
        this.apiKey = apiKey;
    }

    @Override
    public void processPayment(double amount) {
        System.out.printf("[Stripe] Charging $%.2f using key %s%n", amount, apiKey);
    }

    @Override
    public void refund(double amount, String transactionId) {
        System.out.printf("[Stripe] Refunding $%.2f for txn %s%n", amount, transactionId);
    }

    @Override
    public String getGatewayName() { return "Stripe"; }
}

public class RazorpayGateway implements PaymentGateway {
    private final String keyId;
    private final String keySecret;

    public RazorpayGateway(String keyId, String keySecret) {
        this.keyId = keyId;
        this.keySecret = keySecret;
    }

    @Override
    public void processPayment(double amount) {
        System.out.printf("[Razorpay] Charging ₹%.2f%n", amount);
    }

    @Override
    public void refund(double amount, String transactionId) {
        System.out.printf("[Razorpay] Initiating refund ₹%.2f for txn %s%n", amount, transactionId);
    }

    @Override
    public String getGatewayName() { return "Razorpay"; }
}

public class PayPalGateway implements PaymentGateway {
    private final String clientId;

    public PayPalGateway(String clientId) {
        this.clientId = clientId;
    }

    @Override
    public void processPayment(double amount) {
        System.out.printf("[PayPal] Processing $%.2f%n", amount);
    }

    @Override
    public void refund(double amount, String transactionId) {
        System.out.printf("[PayPal] Refunding $%.2f for txn %s%n", amount, transactionId);
    }

    @Override
    public String getGatewayName() { return "PayPal"; }
}

// The abstract creator — defines the factory method
public abstract class PaymentGatewayFactory {
    // Factory method: subclasses implement this to return the right product
    public abstract PaymentGateway createGateway();

    // Template method using the factory method — common behavior
    public void makePayment(double amount) {
        PaymentGateway gateway = createGateway(); // delegate creation to subclass
        System.out.println("Using gateway: " + gateway.getGatewayName());
        gateway.processPayment(amount);
    }
}

// Concrete creators
public class StripeFactory extends PaymentGatewayFactory {
    private final String apiKey;

    public StripeFactory(String apiKey) {
        this.apiKey = apiKey;
    }

    @Override
    public PaymentGateway createGateway() {
        return new StripeGateway(apiKey);
    }
}

public class RazorpayFactory extends PaymentGatewayFactory {
    private final String keyId;
    private final String keySecret;

    public RazorpayFactory(String keyId, String keySecret) {
        this.keyId = keyId;
        this.keySecret = keySecret;
    }

    @Override
    public PaymentGateway createGateway() {
        return new RazorpayGateway(keyId, keySecret);
    }
}

// Usage — caller works with the factory, never with concrete classes
public class PaymentService {
    private final PaymentGatewayFactory factory;

    public PaymentService(PaymentGatewayFactory factory) {
        this.factory = factory;
    }

    public void charge(double amount) {
        factory.makePayment(amount);
    }
}

// Wiring
PaymentGatewayFactory factory = new RazorpayFactory("key_id_123", "secret_abc");
PaymentService service = new PaymentService(factory);
service.charge(1500.00);
// Adding UPI = adding UPIGateway + UPIFactory. Zero modification of existing code.
```

### Simple Factory (Registry-Based) — Common in Interviews

While not a GoF pattern, Simple Factory is practical and frequently asked about:

```java
// Simple Factory using a registry — extensible without if-else chains
public class PaymentGatewayFactory {
    private static final Map<String, Supplier<PaymentGateway>> registry = new HashMap<>();

    static {
        registry.put("STRIPE",   () -> new StripeGateway("stripe_key"));
        registry.put("PAYPAL",   () -> new PayPalGateway("paypal_client"));
        registry.put("RAZORPAY", () -> new RazorpayGateway("rp_key", "rp_secret"));
    }

    // Adding a new gateway: registry.put("UPI", UPIGateway::new)
    public static void register(String type, Supplier<PaymentGateway> supplier) {
        registry.put(type.toUpperCase(), supplier);
    }

    public static PaymentGateway create(String type) {
        Supplier<PaymentGateway> supplier = registry.get(type.toUpperCase());
        if (supplier == null) {
            throw new IllegalArgumentException("Unknown payment gateway: " + type);
        }
        return supplier.get();
    }
}

// Usage
PaymentGateway gateway = PaymentGatewayFactory.create("RAZORPAY");
gateway.processPayment(1500.00);
```

---

## 2.3 Abstract Factory Pattern

### The Problem: Families of Related Objects

Abstract Factory is Factory Method taken one level higher. Instead of creating one type of object, it creates a **family** of related objects that must be used together.

Example: A UI toolkit that must look consistent. Windows UI uses Windows-style buttons, checkboxes, and scrollbars. macOS UI uses macOS-style components. Mixing them breaks visual consistency.

```
GUIFactory (abstract factory interface)
    ├── WindowsFactory → creates WindowsButton, WindowsCheckbox
    └── MacOSFactory  → creates MacOSButton, MacOSCheckbox

Button (abstract product)
    ├── WindowsButton
    └── MacOSButton

Checkbox (abstract product)
    ├── WindowsCheckbox
    └── MacOSCheckbox
```

```java
// Abstract products
public interface Button {
    void render();
    void onClick();
}

public interface Checkbox {
    void render();
    void onCheck(boolean checked);
}

// Windows family
public class WindowsButton implements Button {
    @Override
    public void render() { System.out.println("[Windows] Rendering button with flat style"); }

    @Override
    public void onClick() { System.out.println("[Windows] Button click with system sound"); }
}

public class WindowsCheckbox implements Checkbox {
    @Override
    public void render() { System.out.println("[Windows] Rendering checkbox with square box"); }

    @Override
    public void onCheck(boolean checked) {
        System.out.println("[Windows] Checkbox " + (checked ? "checked" : "unchecked"));
    }
}

// macOS family
public class MacOSButton implements Button {
    @Override
    public void render() { System.out.println("[macOS] Rendering button with rounded corners"); }

    @Override
    public void onClick() { System.out.println("[macOS] Button click with haptic feedback"); }
}

public class MacOSCheckbox implements Checkbox {
    @Override
    public void render() { System.out.println("[macOS] Rendering checkbox with rounded tick"); }

    @Override
    public void onCheck(boolean checked) {
        System.out.println("[macOS] Checkbox " + (checked ? "✓" : "○"));
    }
}

// Abstract factory — declares creation methods for ALL product types in the family
public interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// Concrete factories — each produces a consistent family
public class WindowsFactory implements GUIFactory {
    @Override
    public Button   createButton()   { return new WindowsButton(); }
    @Override
    public Checkbox createCheckbox() { return new WindowsCheckbox(); }
}

public class MacOSFactory implements GUIFactory {
    @Override
    public Button   createButton()   { return new MacOSButton(); }
    @Override
    public Checkbox createCheckbox() { return new MacOSCheckbox(); }
}

// Application uses the factory — it never knows whether it's Windows or macOS
public class Application {
    private final Button button;
    private final Checkbox checkbox;

    public Application(GUIFactory factory) {
        // A MacOSFactory will NEVER accidentally give you a Windows checkbox.
        // The family is guaranteed to be consistent.
        this.button   = factory.createButton();
        this.checkbox = factory.createCheckbox();
    }

    public void renderUI() {
        button.render();
        checkbox.render();
    }
}

// Wiring — determined by runtime environment
GUIFactory factory = System.getProperty("os.name").contains("Mac")
    ? new MacOSFactory()
    : new WindowsFactory();

Application app = new Application(factory);
app.renderUI();
```

**Abstract Factory vs Factory Method:**
- Factory Method creates ONE product, subclasses decide the type
- Abstract Factory creates a FAMILY of products, concrete factory ensures they're compatible

---

## 2.4 Builder Pattern

### The Problem: Telescoping Constructors

```java
// ❌ BEFORE — A User with many optional fields.
// What is the 4th argument? The 7th? You have to count.
public class User {
    public User(String name, String email, String phone,
                String address, String city, String state,
                String zipCode, boolean newsletter, boolean smsAlerts,
                int age, String profilePicUrl) {
        // ...
    }
}

// At the call site, this is a nightmare:
User user = new User(
    "Alice",
    "alice@example.com",
    "+91-9876543210",
    "123 MG Road",
    "Bangalore",
    "Karnataka",
    "560001",
    true,    // newsletter? smsAlerts? nobody knows
    false,
    28,
    null
);
// Bug: true and false are swapped. The compiler won't catch it.
```

**Additional problems:**
- Can't create a User with only required fields without a massive constructor
- Validation happens in the constructor — can't validate incrementally
- Object is mutable if you use setters (thread-safety risk)

---

### Builder Pattern: The Solution

```java
public class User {
    // Immutable fields after construction
    private final String name;         // required
    private final String email;        // required
    private final String phone;        // optional
    private final String address;      // optional
    private final String city;         // optional
    private final String state;        // optional
    private final String zipCode;      // optional
    private final boolean newsletter;  // optional, default false
    private final boolean smsAlerts;   // optional, default false
    private final int age;             // optional
    private final String profilePicUrl; // optional

    // Private constructor — only Builder can call this
    private User(Builder builder) {
        this.name          = builder.name;
        this.email         = builder.email;
        this.phone         = builder.phone;
        this.address       = builder.address;
        this.city          = builder.city;
        this.state         = builder.state;
        this.zipCode       = builder.zipCode;
        this.newsletter    = builder.newsletter;
        this.smsAlerts     = builder.smsAlerts;
        this.age           = builder.age;
        this.profilePicUrl = builder.profilePicUrl;
    }

    // Getters (no setters — this class is immutable)
    public String getName()          { return name; }
    public String getEmail()         { return email; }
    public String getPhone()         { return phone; }
    public String getAddress()       { return address; }
    public String getCity()          { return city; }
    public String getState()         { return state; }
    public boolean isNewsletter()    { return newsletter; }
    public boolean isSmsAlerts()     { return smsAlerts; }
    public int getAge()              { return age; }
    public String getProfilePicUrl() { return profilePicUrl; }

    @Override
    public String toString() {
        return String.format("User{name='%s', email='%s', city='%s', newsletter=%s}",
            name, email, city, newsletter);
    }

    // Static inner Builder class
    public static class Builder {
        // Required fields — set in constructor
        private final String name;
        private final String email;

        // Optional fields — initialized to defaults
        private String phone        = null;
        private String address      = null;
        private String city         = null;
        private String state        = null;
        private String zipCode      = null;
        private boolean newsletter  = false;
        private boolean smsAlerts   = false;
        private int age             = 0;
        private String profilePicUrl = null;

        // Required fields enforced at the constructor level
        public Builder(String name, String email) {
            if (name == null || name.isBlank()) {
                throw new IllegalArgumentException("Name is required");
            }
            if (email == null || !email.contains("@")) {
                throw new IllegalArgumentException("Valid email is required");
            }
            this.name  = name;
            this.email = email;
        }

        // Each setter returns 'this' for chaining
        public Builder phone(String phone) {
            this.phone = phone;
            return this;
        }

        public Builder address(String address) {
            this.address = address;
            return this;
        }

        public Builder city(String city) {
            this.city = city;
            return this;
        }

        public Builder state(String state) {
            this.state = state;
            return this;
        }

        public Builder zipCode(String zipCode) {
            this.zipCode = zipCode;
            return this;
        }

        public Builder newsletter(boolean newsletter) {
            this.newsletter = newsletter;
            return this;
        }

        public Builder smsAlerts(boolean smsAlerts) {
            this.smsAlerts = smsAlerts;
            return this;
        }

        public Builder age(int age) {
            if (age < 0 || age > 150) {
                throw new IllegalArgumentException("Age must be between 0 and 150");
            }
            this.age = age;
            return this;
        }

        public Builder profilePicUrl(String url) {
            this.profilePicUrl = url;
            return this;
        }

        // Terminal method — validates everything, creates the immutable object
        public User build() {
            // Cross-field validation
            if (city != null && state == null) {
                throw new IllegalStateException("State is required when city is provided");
            }
            return new User(this);
        }
    }
}

// ✅ AFTER — Clean, readable, self-documenting
User user = new User.Builder("Alice", "alice@example.com")
    .phone("+91-9876543210")
    .address("123 MG Road")
    .city("Bangalore")
    .state("Karnataka")
    .zipCode("560001")
    .newsletter(true)   // Now obviously labeled
    .smsAlerts(false)
    .age(28)
    .build();

// Minimal user — only required fields
User minimalUser = new User.Builder("Bob", "bob@example.com")
    .build();
```

### Lombok @Builder

In production Spring Boot code, Lombok eliminates all the boilerplate:

```java
import lombok.Builder;
import lombok.Getter;
import lombok.NonNull;

@Builder
@Getter
public class User {
    @NonNull private final String name;    // @NonNull generates null check in builder
    @NonNull private final String email;
    private final String phone;
    private final String city;
    private final String state;
    @Builder.Default private final boolean newsletter = false; // default value
    @Builder.Default private final boolean smsAlerts  = false;
}

// Lombok generates the Builder with ALL the method-chaining boilerplate.
// Usage is identical:
User user = User.builder()
    .name("Alice")
    .email("alice@example.com")
    .city("Bangalore")
    .newsletter(true)
    .build();
```

**What Lombok generates for you:**
- Inner static `Builder` class
- All the setter-chain methods
- `build()` method
- `@NonNull` fields get null checks in the builder

---

## 2.5 Prototype Pattern

### The Problem: Expensive Object Creation

Some objects are expensive to create:
- Database query results
- HTTP API responses
- Complex objects with many fields

Instead of creating from scratch, clone an existing instance.

### Shallow Copy vs Deep Copy

```java
// The prototype interface (Java provides Cloneable, but interface is cleaner)
public interface Prototype<T> {
    T copy();
}

// Example: A complex document template
public class DocumentTemplate implements Prototype<DocumentTemplate> {
    private String title;
    private String author;
    private List<String> sections; // mutable — needs careful copying
    private Map<String, String> metadata;

    public DocumentTemplate(String title, String author) {
        this.title    = title;
        this.author   = author;
        this.sections = new ArrayList<>();
        this.metadata = new HashMap<>();
    }

    // SHALLOW COPY — sections list is shared between original and copy!
    // Modifying one copy's sections affects the other.
    public DocumentTemplate shallowCopy() {
        DocumentTemplate copy = new DocumentTemplate(this.title, this.author);
        copy.sections = this.sections; // same reference! ← bug
        copy.metadata = this.metadata; // same reference! ← bug
        return copy;
    }

    // DEEP COPY — completely independent object
    @Override
    public DocumentTemplate copy() {
        DocumentTemplate copy = new DocumentTemplate(this.title, this.author);
        copy.sections = new ArrayList<>(this.sections); // new list with same strings
        copy.metadata = new HashMap<>(this.metadata);   // new map with same entries
        return copy;
    }

    public void addSection(String section) { sections.add(section); }
    public void setMetadata(String key, String value) { metadata.put(key, value); }

    public List<String> getSections() { return Collections.unmodifiableList(sections); }

    @Override
    public String toString() {
        return "DocumentTemplate{title='" + title + "', sections=" + sections + "}";
    }
}

// A prototype registry — store pre-configured prototypes, clone on demand
public class TemplateRegistry {
    private final Map<String, DocumentTemplate> templates = new HashMap<>();

    public void register(String name, DocumentTemplate template) {
        templates.put(name, template);
    }

    public DocumentTemplate getTemplate(String name) {
        DocumentTemplate template = templates.get(name);
        if (template == null) {
            throw new IllegalArgumentException("No template registered: " + name);
        }
        return template.copy(); // always return a COPY, not the original
    }
}

// Usage
DocumentTemplate invoiceTemplate = new DocumentTemplate("Invoice", "System");
invoiceTemplate.addSection("Header");
invoiceTemplate.addSection("Line Items");
invoiceTemplate.addSection("Tax Summary");
invoiceTemplate.addSection("Footer");

TemplateRegistry registry = new TemplateRegistry();
registry.register("INVOICE", invoiceTemplate);

// Create new invoices from the prototype — fast, no DB calls
DocumentTemplate invoice1 = registry.getTemplate("INVOICE");
invoice1.addSection("Custom Section for Order #1001"); // Only affects this copy

DocumentTemplate invoice2 = registry.getTemplate("INVOICE");
invoice2.setMetadata("customer", "Alice"); // Only affects this copy

System.out.println(invoice1.getSections()); // [Header, Line Items, Tax Summary, Footer, Custom Section for Order #1001]
System.out.println(invoice2.getSections()); // [Header, Line Items, Tax Summary, Footer] — unchanged
```

**When to use Prototype:**
- Object creation is expensive (many DB calls, complex initialization)
- You need many similar objects with slight variations
- You want to hide the concrete type from the client

**When NOT to use Prototype:**
- When shallow copy is sufficient — don't over-engineer deep copy
- When the object has no expensive-to-replicate state

---

## Chapter 2 Summary

| Pattern | Intent | Key Benefit | Interview Trigger |
|---------|--------|-------------|------------------|
| Singleton | One instance, globally accessible | No duplicate resource management | Config, connection pool, logger |
| Factory Method | Subclass decides which class to instantiate | OCP: add products without modifying factory | Multiple implementations of same interface |
| Abstract Factory | Consistent family of products | Can't accidentally mix incompatible objects | Platform-specific UI, theme engines |
| Builder | Step-by-step construction with validation | Readable creation of complex objects | Objects with many optional fields |
| Prototype | Clone instead of construct | Performance for expensive initialization | Template systems, object pools |

### Interview Questions on Creational Patterns

**Q: What's the difference between Singleton and static class?**
A: A static class can't implement interfaces, can't be passed as a parameter, can't be lazily initialized, and can't use polymorphism. Singleton is a design pattern for an instance; static class is a namespace.

**Q: Why is enum singleton better than double-checked locking?**
A: Less boilerplate, immune to reflection and serialization attacks, guaranteed thread safety by JVM spec.

**Q: When would you use Builder vs just setters on a POJO?**
A: Builder enables immutability (no setters after construction), validates during build (not scattered across the code), and reads more clearly when you have many optional parameters. POJOs with setters are mutable and don't validate consistency.

**Q: What's the difference between Factory Method and Abstract Factory?**
A: Factory Method creates one product, the subclass decides the type. Abstract Factory creates a family of related products and guarantees they're compatible with each other.
