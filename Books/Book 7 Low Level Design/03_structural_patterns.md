# Chapter 3: Structural Patterns

> Structural patterns deal with object composition — how classes and objects are combined to form larger structures while keeping the structure flexible and efficient.

---

## 3.1 Adapter Pattern

### The Problem: Incompatible Interfaces

You have a system that expects an interface of type `A`. You have a third-party library or legacy code that provides type `B`. You can't modify either. You need a bridge.

Classic cases:
- Third-party payment SDK with different method signatures than your interface
- Legacy database layer with raw JDBC that needs to fit behind a repository interface
- External API client that returns XML, but your code expects JSON objects

### ❌ Before — Incompatible Interfaces Forced Together

```java
// YOUR system's interface — what your code expects
public interface CurrencyConverter {
    double convert(String fromCurrency, String toCurrency, double amount);
}

// LEGACY third-party code — different signature, can't be changed
public class LegacyCurrencyService {
    // Different parameter order, returns a formatted string instead of double
    public String getExchangeRate(double amount, String source, String target) {
        // Simulated conversion
        double rate = source.equals("USD") && target.equals("INR") ? 83.5 : 1.0;
        return String.format("%.2f %s", amount * rate, target);
    }
}

// PROBLEM: You can't pass LegacyCurrencyService where CurrencyConverter is expected.
// If you change your code everywhere to use LegacyCurrencyService directly,
// you're tightly coupled to a legacy API that might change.
```

### ✅ After — Adapter Bridges the Gap

```java
// The target interface — unchanged
public interface CurrencyConverter {
    double convert(String fromCurrency, String toCurrency, double amount);
}

// The legacy service — unchanged (it's third-party)
public class LegacyCurrencyService {
    public String getExchangeRate(double amount, String source, String target) {
        double rate = source.equals("USD") && target.equals("INR") ? 83.5 : 1.0;
        return String.format("%.2f %s", amount * rate, target);
    }
}

// THE ADAPTER: wraps LegacyCurrencyService, exposes CurrencyConverter interface
public class LegacyCurrencyAdapter implements CurrencyConverter {
    private final LegacyCurrencyService legacyService;

    public LegacyCurrencyAdapter(LegacyCurrencyService legacyService) {
        this.legacyService = legacyService;
    }

    @Override
    public double convert(String fromCurrency, String toCurrency, double amount) {
        // Adapt: reorder parameters, transform the return type
        String result = legacyService.getExchangeRate(amount, fromCurrency, toCurrency);
        // Parse "1247.50 INR" → 1247.50
        return Double.parseDouble(result.split(" ")[0]);
    }
}

// A modern alternative to the legacy service
public class ExchangeRateApiClient implements CurrencyConverter {
    @Override
    public double convert(String fromCurrency, String toCurrency, double amount) {
        // Modern API call
        System.out.printf("Calling modern exchange rate API: %s → %s%n", fromCurrency, toCurrency);
        return amount * 83.5; // simplified
    }
}

// Your business code — works with the interface, doesn't care about the implementation
public class InvoiceService {
    private final CurrencyConverter converter;

    public InvoiceService(CurrencyConverter converter) { // Depends on interface
        this.converter = converter;
    }

    public double generateInvoice(double amountUSD) {
        double amountINR = converter.convert("USD", "INR", amountUSD);
        System.out.printf("Invoice: $%.2f USD = ₹%.2f INR%n", amountUSD, amountINR);
        return amountINR;
    }
}

// Usage — swap legacy for modern without changing InvoiceService
LegacyCurrencyService legacyService = new LegacyCurrencyService();
CurrencyConverter adapter = new LegacyCurrencyAdapter(legacyService);
InvoiceService invoiceService = new InvoiceService(adapter);
invoiceService.generateInvoice(100.0); // works via adapter

// Later, replace with modern client:
InvoiceService invoiceService2 = new InvoiceService(new ExchangeRateApiClient());
invoiceService2.generateInvoice(100.0); // works with modern client
```

**Adapter vs Bridge:**
- Adapter: fixes an incompatibility that already exists (retrospective)
- Bridge: separates abstraction from implementation before the problem occurs (proactive)

---

## 3.2 Decorator Pattern

### The Problem: Adding Behavior Without Modification

You want to add logging, caching, retry, or timing to a service — but:
- You can't modify the service (it's in a library or you don't want to change it)
- Subclassing is impractical (you'd need `LoggingAndCachingService`, `LoggingService`, `CachingService`, etc. — combinatorial explosion)
- You want to add/remove behaviors at runtime

### Java I/O as Real-World Decorator

Java's I/O library is the textbook example:
```java
// Each wrapper ADDS behavior, delegates core work to the wrapped object
InputStream raw     = new FileInputStream("data.txt");   // base: reads bytes from file
InputStream buffered = new BufferedInputStream(raw);       // adds: buffering
InputStream gzipped  = new GZIPInputStream(buffered);      // adds: decompression
InputStreamReader reader = new InputStreamReader(gzipped); // adds: byte→char conversion
BufferedReader br = new BufferedReader(reader);             // adds: line-by-line reading

// Each class is a decorator — it wraps another InputStream and adds one behavior.
String line = br.readLine(); // Reads from file, in chunks, decompresses, decodes, buffers lines
```

### Full Example: Coffee with Decorators

```java
// Component interface — the thing being decorated
public interface Coffee {
    double getCost();
    String getDescription();
}

// Concrete component — the base object
public class SimpleCoffee implements Coffee {
    @Override
    public double getCost() { return 30.0; } // ₹30

    @Override
    public String getDescription() { return "Simple Coffee"; }
}

// Abstract decorator — wraps a Coffee, delegates to it
public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee coffee; // the wrapped object

    protected CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }

    @Override
    public double getCost() { return coffee.getCost(); } // delegate

    @Override
    public String getDescription() { return coffee.getDescription(); } // delegate
}

// Concrete decorators — each adds ONE behavior
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double getCost() {
        return coffee.getCost() + 10.0; // add milk cost
    }

    @Override
    public String getDescription() {
        return coffee.getDescription() + ", Milk";
    }
}

public class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double getCost() {
        return coffee.getCost() + 5.0;
    }

    @Override
    public String getDescription() {
        return coffee.getDescription() + ", Sugar";
    }
}

public class CaramelDecorator extends CoffeeDecorator {
    public CaramelDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double getCost() {
        return coffee.getCost() + 20.0;
    }

    @Override
    public String getDescription() {
        return coffee.getDescription() + ", Caramel";
    }
}

public class WhipDecorator extends CoffeeDecorator {
    public WhipDecorator(Coffee coffee) { super(coffee); }

    @Override
    public double getCost() {
        return coffee.getCost() + 15.0;
    }

    @Override
    public String getDescription() {
        return coffee.getDescription() + ", Whip";
    }
}

// Usage — compose decorators at runtime
Coffee order1 = new SimpleCoffee();
order1 = new MilkDecorator(order1);
order1 = new SugarDecorator(order1);
System.out.printf("%-35s ₹%.2f%n", order1.getDescription(), order1.getCost());
// Simple Coffee, Milk, Sugar   ₹45.00

Coffee order2 = new SimpleCoffee();
order2 = new MilkDecorator(order2);
order2 = new CaramelDecorator(order2);
order2 = new WhipDecorator(order2);
System.out.printf("%-35s ₹%.2f%n", order2.getDescription(), order2.getCost());
// Simple Coffee, Milk, Caramel, Whip   ₹75.00
```

### Practical Decorator: Adding Logging and Caching to a Service

```java
public interface UserRepository {
    User findById(Long id);
    void save(User user);
}

public class DatabaseUserRepository implements UserRepository {
    @Override
    public User findById(Long id) {
        System.out.println("DB query: SELECT * FROM users WHERE id = " + id);
        return new User("Alice", "alice@example.com"); // simulated
    }

    @Override
    public void save(User user) {
        System.out.println("DB query: INSERT/UPDATE user " + user.getName());
    }
}

// Logging decorator
public class LoggingUserRepository implements UserRepository {
    private final UserRepository delegate;

    public LoggingUserRepository(UserRepository delegate) {
        this.delegate = delegate;
    }

    @Override
    public User findById(Long id) {
        System.out.println("[LOG] findById called with id=" + id);
        long start = System.currentTimeMillis();
        User result = delegate.findById(id);
        System.out.println("[LOG] findById completed in " + (System.currentTimeMillis() - start) + "ms");
        return result;
    }

    @Override
    public void save(User user) {
        System.out.println("[LOG] save called for user=" + user.getName());
        delegate.save(user);
    }
}

// Caching decorator
public class CachingUserRepository implements UserRepository {
    private final UserRepository delegate;
    private final Map<Long, User> cache = new ConcurrentHashMap<>();

    public CachingUserRepository(UserRepository delegate) {
        this.delegate = delegate;
    }

    @Override
    public User findById(Long id) {
        return cache.computeIfAbsent(id, delegate::findById);
    }

    @Override
    public void save(User user) {
        delegate.save(user);
        cache.clear(); // invalidate cache on write
    }
}

// Stack decorators — logging wraps caching wraps database
UserRepository repo =
    new LoggingUserRepository(
        new CachingUserRepository(
            new DatabaseUserRepository()
        )
    );

repo.findById(1L); // [LOG] findById → cache miss → DB query
repo.findById(1L); // [LOG] findById → cache hit → no DB query
```

---

## 3.3 Proxy Pattern

### The Three Proxy Types

A Proxy controls access to another object. Same interface as the real object, adds a layer of control.

**1. Virtual Proxy (Lazy Loading)**
**2. Protection Proxy (Access Control)**
**3. Remote Proxy (hides network communication)**

### Caching Proxy

```java
public interface WeatherService {
    String getCurrentWeather(String city);
}

public class RealWeatherService implements WeatherService {
    @Override
    public String getCurrentWeather(String city) {
        System.out.println("[API Call] Fetching weather for " + city);
        // Expensive HTTP call — simulated
        return "Sunny, 28°C";
    }
}

public class CachingWeatherProxy implements WeatherService {
    private final WeatherService realService;
    private final Map<String, String> cache = new HashMap<>();
    private final Map<String, Long> cacheTimestamps = new HashMap<>();
    private static final long CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

    public CachingWeatherProxy(WeatherService realService) {
        this.realService = realService;
    }

    @Override
    public String getCurrentWeather(String city) {
        String cached = cache.get(city);
        Long timestamp = cacheTimestamps.get(city);

        if (cached != null && timestamp != null
                && (System.currentTimeMillis() - timestamp) < CACHE_TTL_MS) {
            System.out.println("[Cache Hit] " + city);
            return cached;
        }

        System.out.println("[Cache Miss] " + city + " — calling real service");
        String result = realService.getCurrentWeather(city);
        cache.put(city, result);
        cacheTimestamps.put(city, System.currentTimeMillis());
        return result;
    }
}
```

### Security Proxy

```java
public interface AdminService {
    void deleteUser(Long userId);
    void viewAuditLog();
    List<User> listAllUsers();
}

public class RealAdminService implements AdminService {
    @Override
    public void deleteUser(Long userId) { System.out.println("Deleted user " + userId); }

    @Override
    public void viewAuditLog() { System.out.println("Viewing audit log..."); }

    @Override
    public List<User> listAllUsers() { return List.of(); }
}

public class SecurityAdminProxy implements AdminService {
    private final AdminService realService;
    private final Set<String> currentUserRoles;

    public SecurityAdminProxy(AdminService realService, Set<String> roles) {
        this.realService = realService;
        this.currentUserRoles = roles;
    }

    private void requireRole(String role) {
        if (!currentUserRoles.contains(role)) {
            throw new SecurityException("Access denied: requires role " + role);
        }
    }

    @Override
    public void deleteUser(Long userId) {
        requireRole("SUPER_ADMIN");
        realService.deleteUser(userId);
    }

    @Override
    public void viewAuditLog() {
        requireRole("AUDITOR");
        realService.viewAuditLog();
    }

    @Override
    public List<User> listAllUsers() {
        requireRole("ADMIN");
        return realService.listAllUsers();
    }
}
```

### Spring's @Transactional as a Proxy

```java
// Spring creates a proxy around your service.
// The proxy intercepts method calls and wraps them in a transaction.
@Service
public class OrderService {
    @Transactional  // Spring creates a proxy around this method
    public void placeOrder(Order order) {
        orderRepository.save(order);
        inventoryService.decreaseStock(order.getItemId());
        // If inventoryService.decreaseStock() throws, Spring's proxy
        // calls connection.rollback() automatically.
    }
}

// What Spring generates (simplified):
public class OrderServiceProxy extends OrderService {
    @Override
    public void placeOrder(Order order) {
        Connection conn = dataSource.getConnection();
        conn.setAutoCommit(false);
        try {
            super.placeOrder(order); // delegate to real method
            conn.commit();
        } catch (Exception e) {
            conn.rollback();
            throw e;
        }
    }
}
```

---

## 3.4 Facade Pattern

### The Problem: Complex Subsystem, Simple Client

A video processing service has many components: video decoding, audio extraction, thumbnail generation, format conversion, upload to S3, database record creation, and CDN cache invalidation. The client shouldn't know about all of these — it just wants to "process a video."

```java
// The complex subsystem — many classes, each doing one thing
public class VideoDecoder {
    public RawVideoData decode(byte[] data) {
        System.out.println("Decoding video bytes...");
        return new RawVideoData();
    }
}

public class AudioExtractor {
    public AudioTrack extract(RawVideoData rawVideo) {
        System.out.println("Extracting audio track...");
        return new AudioTrack();
    }
}

public class ThumbnailGenerator {
    public byte[] generate(RawVideoData rawVideo, int second) {
        System.out.println("Generating thumbnail at second " + second);
        return new byte[0];
    }
}

public class VideoEncoder {
    public EncodedVideo encode(RawVideoData rawVideo, String format) {
        System.out.println("Encoding video to " + format + " format...");
        return new EncodedVideo();
    }
}

public class S3Uploader {
    public String upload(EncodedVideo video) {
        System.out.println("Uploading to S3...");
        return "https://cdn.example.com/videos/abc123.mp4";
    }

    public String uploadThumbnail(byte[] thumbnail) {
        System.out.println("Uploading thumbnail to S3...");
        return "https://cdn.example.com/thumbs/abc123.jpg";
    }
}

public class VideoMetadataRepository {
    public void save(VideoMetadata metadata) {
        System.out.println("Saving video metadata to DB...");
    }
}

// ❌ WITHOUT FACADE — Client must coordinate ALL of this
public class UploadController {
    private VideoDecoder decoder = new VideoDecoder();
    private AudioExtractor extractor = new AudioExtractor();
    private ThumbnailGenerator thumbGen = new ThumbnailGenerator();
    private VideoEncoder encoder = new VideoEncoder();
    private S3Uploader uploader = new S3Uploader();
    private VideoMetadataRepository metaRepo = new VideoMetadataRepository();

    public void handleUpload(byte[] rawData, String title) {
        // Client must know the entire pipeline
        RawVideoData rawVideo = decoder.decode(rawData);
        AudioTrack audio      = extractor.extract(rawVideo);
        byte[] thumbnail      = thumbGen.generate(rawVideo, 5);
        EncodedVideo mp4      = encoder.encode(rawVideo, "mp4");
        String videoUrl       = uploader.upload(mp4);
        String thumbUrl       = uploader.uploadThumbnail(thumbnail);
        VideoMetadata meta    = new VideoMetadata(title, videoUrl, thumbUrl);
        metaRepo.save(meta);
        // 7 steps. What if the order changes? Every client must be updated.
    }
}
```

```java
// ✅ THE FACADE — single entry point, hides all complexity
public class VideoProcessingFacade {
    private final VideoDecoder decoder;
    private final AudioExtractor extractor;
    private final ThumbnailGenerator thumbGen;
    private final VideoEncoder encoder;
    private final S3Uploader uploader;
    private final VideoMetadataRepository metaRepo;

    public VideoProcessingFacade(VideoDecoder decoder, AudioExtractor extractor,
                                  ThumbnailGenerator thumbGen, VideoEncoder encoder,
                                  S3Uploader uploader, VideoMetadataRepository metaRepo) {
        this.decoder   = decoder;
        this.extractor = extractor;
        this.thumbGen  = thumbGen;
        this.encoder   = encoder;
        this.uploader  = uploader;
        this.metaRepo  = metaRepo;
    }

    // Simple, intent-revealing method for clients
    public VideoMetadata processAndUpload(byte[] rawData, String title) {
        RawVideoData rawVideo = decoder.decode(rawData);
        extractor.extract(rawVideo); // audio processing for later use
        byte[] thumbnail      = thumbGen.generate(rawVideo, 5);
        EncodedVideo mp4      = encoder.encode(rawVideo, "mp4");
        String videoUrl       = uploader.upload(mp4);
        String thumbUrl       = uploader.uploadThumbnail(thumbnail);
        VideoMetadata meta    = new VideoMetadata(title, videoUrl, thumbUrl);
        metaRepo.save(meta);
        return meta;
    }
}

// ✅ Clean controller — doesn't know about subsystem complexity
@RestController
public class UploadController {
    private final VideoProcessingFacade facade;

    public UploadController(VideoProcessingFacade facade) {
        this.facade = facade;
    }

    @PostMapping("/upload")
    public VideoMetadata upload(@RequestBody UploadRequest req) {
        return facade.processAndUpload(req.getData(), req.getTitle());
    }
}
```

**Facade vs Adapter:**
- Adapter makes an existing interface compatible with another (fixes incompatibility)
- Facade creates a NEW, simpler interface to a complex subsystem (reduces complexity)

---

## 3.5 Composite Pattern

### The Problem: Uniform Treatment of Trees

File systems, menus, UI components, and organizational hierarchies all share a structure: individual items and containers of items. Clients should be able to treat both uniformly — "calculate total size" should work whether you call it on a file or a directory.

```
FileSystemComponent (interface/abstract)
    ├── File         (leaf)
    └── Directory    (composite — contains FileSystemComponents)
```

```java
// Component interface — leaf and composite share this
public interface FileSystemComponent {
    String getName();
    long getSize();         // For file: file size. For directory: sum of children.
    void print(String indent);
}

// Leaf — no children
public class File implements FileSystemComponent {
    private final String name;
    private final long size; // bytes

    public File(String name, long size) {
        this.name = name;
        this.size = size;
    }

    @Override
    public String getName() { return name; }

    @Override
    public long getSize() { return size; }

    @Override
    public void print(String indent) {
        System.out.printf("%s📄 %s (%d bytes)%n", indent, name, size);
    }
}

// Composite — contains other FileSystemComponents (files OR directories)
public class Directory implements FileSystemComponent {
    private final String name;
    private final List<FileSystemComponent> children = new ArrayList<>();

    public Directory(String name) {
        this.name = name;
    }

    public void add(FileSystemComponent component) {
        children.add(component);
    }

    public void remove(FileSystemComponent component) {
        children.remove(component);
    }

    @Override
    public String getName() { return name; }

    @Override
    public long getSize() {
        // Recursively sums children — works regardless of depth
        return children.stream().mapToLong(FileSystemComponent::getSize).sum();
    }

    @Override
    public void print(String indent) {
        System.out.printf("%s📁 %s (%d bytes total)%n", indent, name, getSize());
        for (FileSystemComponent child : children) {
            child.print(indent + "  "); // recurse
        }
    }
}

// Usage
Directory root = new Directory("root");
Directory src = new Directory("src");
Directory main = new Directory("main");
Directory test = new Directory("test");

main.add(new File("App.java", 2048));
main.add(new File("UserService.java", 4096));
main.add(new File("OrderService.java", 3500));

test.add(new File("AppTest.java", 1200));
test.add(new File("UserServiceTest.java", 2800));

src.add(main);
src.add(test);

root.add(src);
root.add(new File("pom.xml", 512));
root.add(new File("README.md", 1024));

root.print("");
System.out.println("Total project size: " + root.getSize() + " bytes");
```

**Output:**
```
📁 root (15180 bytes total)
  📁 src (13644 bytes total)
    📁 main (9644 bytes total)
      📄 App.java (2048 bytes)
      📄 UserService.java (4096 bytes)
      📄 OrderService.java (3500 bytes)
    📁 test (4000 bytes total)
      📄 AppTest.java (1200 bytes)
      📄 UserServiceTest.java (2800 bytes)
  📄 pom.xml (512 bytes)
  📄 README.md (1024 bytes)
Total project size: 15180 bytes
```

**When to use Composite:**
- You have a tree structure of objects
- You want clients to treat individual objects and compositions uniformly
- The "part-whole" hierarchy is the core data model

---

## 3.6 Flyweight Pattern

### Intent: Share Immutable State to Save Memory

```java
// ════════════════════════════════════════════════════════════════════════════
// FLYWEIGHT PATTERN — BEFORE Code
// ════════════════════════════════════════════════════════════════════════════

// ── BEFORE: The memory catastrophe ───────────────────────────────────────────
//
// A text editor renders 1 million characters. Without Flyweight, we create
// a FontConfig object for each character. Each FontConfig uses ~200 bytes.
// 1,000,000 characters × 200 bytes = 200MB just for font objects.
// The JVM heap overflows. The application crashes.

public class TextEditor_BEFORE {

    public void renderDocument(String text) {
        List<CharacterGlyph> glyphs = new ArrayList<>();

        for (int i = 0; i < text.length(); i++) {
            // PROBLEM: creating a NEW FontConfig object for EVERY character
            // Even if the same font is used for all characters, we make a million copies
            FontConfig font = new FontConfig("Arial", 12, Color.BLACK, false, false);
            //                 ↑ 200 bytes × 1,000,000 = 200MB of identical objects

            glyphs.add(new CharacterGlyph(text.charAt(i), font, i));
        }
        // Memory: 200MB for font objects alone
        // Time: 1,000,000 object allocations + GC pressure
    }
}

// ── AFTER: Flyweight — share intrinsic state ──────────────────────────────────
//
// Key insight: FontConfig("Arial", 12, BLACK) is the same for every character.
// Why create 1,000,000 identical objects? Create ONE and share it.
// The POSITION (extrinsic state) is different per character — pass it separately.

public class FontConfigFactory {
    // Cache: key = "fontName-size-colorHex-bold-italic", value = shared FontConfig
    private static final Map<String, FontConfig> cache = new ConcurrentHashMap<>();

    public static FontConfig get(String name, int size, Color color, boolean bold, boolean italic) {
        String key = name + "-" + size + "-" + color.getRGB() + "-" + bold + "-" + italic;
        // computeIfAbsent is atomic: creates the FontConfig ONLY if not already cached
        return cache.computeIfAbsent(key, k -> new FontConfig(name, size, color, bold, italic));
    }

    public static int getCacheSize() { return cache.size(); }
}

public class TextEditor_AFTER {

    public void renderDocument(String text) {
        // Get the shared FontConfig ONCE (or once per unique font combination)
        FontConfig sharedFont = FontConfigFactory.get("Arial", 12, Color.BLACK, false, false);
        //          ↑ one object, no matter how many characters use it

        List<CharacterGlyph> glyphs = new ArrayList<>();
        for (int i = 0; i < text.length(); i++) {
            // Intrinsic state (font properties): SHARED via sharedFont reference
            // Extrinsic state (position): PASSED as method parameter
            glyphs.add(new CharacterGlyph(text.charAt(i), sharedFont, i));
        }
        // Memory: 200 bytes (1 FontConfig) instead of 200MB
        // Objects created: 1 instead of 1,000,000
    }
}

// Real-world usage: Java String pool is Flyweight
// "hello" == "hello" is true because both are the SAME object from the pool
// String.intern() explicitly adds a string to the Flyweight pool

// When to use Flyweight:
// - Creating massive numbers of fine-grained objects
// - Objects share most of their state
// - External state can be passed to operations rather than stored
// - Memory is the bottleneck
```

---

## Chapter 3 Summary

| Pattern | Analogy | Intent | Key Design |
|---------|---------|--------|------------|
| Adapter | Power plug adapter | Bridge incompatible interfaces | Wraps old, exposes new |
| Decorator | Coffee with toppings | Add behavior without modifying | Wraps same interface, adds behavior |
| Proxy | Personal assistant | Control access to an object | Wraps real object, intercepts calls |
| Facade | Hotel concierge | Simplify a complex subsystem | Single entry point, hides complexity |
| Composite | File system | Treat leaf and container uniformly | Tree structure, recursive operations |
| Flyweight | Font cache | Share immutable state across many objects | Factory + cache, intrinsic vs extrinsic |

### Interview Questions on Structural Patterns

**Q: What is the difference between Decorator and Proxy?**
A: Both wrap objects. Decorator adds new behavior visible to the client (the coffee gets more expensive). Proxy controls access and adds cross-cutting concerns transparent to the client (the client doesn't know about caching — it just gets weather).

**Q: Decorator vs Inheritance for adding behavior?**
A: Inheritance is static — you must decide at compile time. Decorator is dynamic — you can compose behaviors at runtime. Also, inheritance creates M×N subclasses for M base classes and N behaviors; Decorator requires only M + N classes.

**Q: Where does Spring use Proxy?**
A: `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` — all implemented as AOP proxies that intercept method calls and add behavior.

**Q: When would you NOT use Facade?**
A: When the client legitimately needs fine-grained control over the subsystem. Facade trades flexibility for simplicity. If one client needs step 3 but not step 5, a facade that runs all 7 steps is inappropriate.
