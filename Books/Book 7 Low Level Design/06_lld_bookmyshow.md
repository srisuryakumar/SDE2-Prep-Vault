# Chapter 6: LLD Design 2 — BookMyShow (Movie Ticket Booking)

> This is the hardest of the common LLD designs because it involves a critical concurrency problem: two users clicking "Book" on the same seat at the same millisecond.

---

## Step 1: Requirements Gathering

**Functional Requirements:**
- Search movies by city, date, genre
- Browse theatres and available shows
- Select specific seats on a seat map
- Book seats (up to 10 per transaction)
- Hold seats for up to 10 minutes during payment
- Release held seats if payment times out
- Handle concurrent bookings for the same seat

**Non-Functional Requirements:**
- Seat A5 must never be double-booked — correctness is paramount
- Flash sale: 100K users try to book simultaneously
- Hold must auto-expire without manual intervention

---

## Step 2: Entities and Relationships

```
Movie
    ← has many → Show
         ← has one → Screen
              ← has many → Seat
                   ← has one → SeatBooking (state: AVAILABLE/HELD/BOOKED)

User ← creates → Booking
Booking ← contains many → SeatBooking
       ← has one → Payment
```

---

## Step 3: Seat State Machine

This is the core of BookMyShow's concurrency model:

```
AVAILABLE ──── User selects ────► HELD (TTL: 10 min)
    ▲                                    │
    │                                    │ Payment succeeds
    │ TTL expires / User cancels         ▼
    └──────────────────────────── BOOKED
```

---

## Step 4: Full Java Implementation

```java
// ── Core Enums ────────────────────────────────────────────────────────────

public enum SeatType   { REGULAR, PREMIUM, RECLINER, WHEELCHAIR }
public enum SeatStatus { AVAILABLE, HELD, BOOKED }
public enum BookingStatus { PENDING, CONFIRMED, CANCELLED, EXPIRED }
public enum Genre { ACTION, COMEDY, DRAMA, THRILLER, HORROR }
```

```java
// ── Movie ─────────────────────────────────────────────────────────────────

public class Movie {
    private final String movieId;
    private final String title;
    private final String language;
    private final int durationMinutes;
    private final Genre genre;
    private final String description;

    public Movie(String movieId, String title, String language,
                 int durationMinutes, Genre genre) {
        this.movieId         = movieId;
        this.title           = title;
        this.language        = language;
        this.durationMinutes = durationMinutes;
        this.genre           = genre;
        this.description     = "";
    }

    public String getMovieId()          { return movieId; }
    public String getTitle()            { return title; }
    public String getLanguage()         { return language; }
    public int getDurationMinutes()     { return durationMinutes; }
    public Genre getGenre()             { return genre; }

    @Override
    public String toString() {
        return String.format("Movie{%s, %s, %s, %dmin}", movieId, title, language, durationMinutes);
    }
}
```

```java
// ── Theatre and Screen ────────────────────────────────────────────────────

public class Theatre {
    private final String theatreId;
    private final String name;
    private final String city;
    private final String address;
    private final List<Screen> screens;

    public Theatre(String theatreId, String name, String city, String address) {
        this.theatreId = theatreId;
        this.name      = name;
        this.city      = city;
        this.address   = address;
        this.screens   = new ArrayList<>();
    }

    public void addScreen(Screen screen) { screens.add(screen); }

    public String getTheatreId()   { return theatreId; }
    public String getName()        { return name; }
    public String getCity()        { return city; }
    public List<Screen> getScreens() { return Collections.unmodifiableList(screens); }
}

public class Screen {
    private final String screenId;
    private final String name;         // "Audi 1", "IMAX Hall"
    private final int totalSeats;
    private final Theatre theatre;
    private final List<Seat> seats;

    public Screen(String screenId, String name, int totalSeats, Theatre theatre) {
        this.screenId   = screenId;
        this.name       = name;
        this.totalSeats = totalSeats;
        this.theatre    = theatre;
        this.seats      = new ArrayList<>();
    }

    public void addSeat(Seat seat) { seats.add(seat); }

    public String getScreenId()   { return screenId; }
    public String getName()       { return name; }
    public Theatre getTheatre()   { return theatre; }
    public List<Seat> getSeats()  { return Collections.unmodifiableList(seats); }
}
```

```java
// ── Seat ─────────────────────────────────────────────────────────────────

public class Seat {
    private final String seatId;    // e.g., "A5", "C12"
    private final String row;       // "A", "B", "C"
    private final int number;       // 5, 12
    private final SeatType type;
    private final double basePrice;
    private final Screen screen;

    public Seat(String seatId, String row, int number,
                SeatType type, double basePrice, Screen screen) {
        this.seatId    = seatId;
        this.row       = row;
        this.number    = number;
        this.type      = type;
        this.basePrice = basePrice;
        this.screen    = screen;
    }

    public String getSeatId()    { return seatId; }
    public String getRow()       { return row; }
    public int getNumber()       { return number; }
    public SeatType getType()    { return type; }
    public double getBasePrice() { return basePrice; }
    public Screen getScreen()    { return screen; }

    @Override
    public String toString() { return seatId + "(" + type + ")"; }
}
```

```java
// ── Show ──────────────────────────────────────────────────────────────────

public class Show {
    private final String showId;
    private final Movie movie;
    private final Screen screen;
    private final LocalDateTime startTime;
    private final LocalDateTime endTime;
    private final Map<String, ShowSeat> showSeats; // seatId → ShowSeat

    public Show(String showId, Movie movie, Screen screen, LocalDateTime startTime) {
        this.showId    = showId;
        this.movie     = movie;
        this.screen    = screen;
        this.startTime = startTime;
        this.endTime   = startTime.plusMinutes(movie.getDurationMinutes());
        this.showSeats = new ConcurrentHashMap<>();

        // Initialize show seats from screen seats
        for (Seat seat : screen.getSeats()) {
            showSeats.put(seat.getSeatId(), new ShowSeat(seat, this));
        }
    }

    public String getShowId()                 { return showId; }
    public Movie getMovie()                   { return movie; }
    public Screen getScreen()                 { return screen; }
    public LocalDateTime getStartTime()       { return startTime; }
    public Map<String, ShowSeat> getShowSeats() { return showSeats; }

    public List<ShowSeat> getAvailableSeats() {
        return showSeats.values().stream()
            .filter(ss -> ss.getStatus() == SeatStatus.AVAILABLE)
            .collect(java.util.stream.Collectors.toList());
    }
}
```

```java
// ── ShowSeat (the booking unit with state) ────────────────────────────────

public class ShowSeat {
    private final Seat seat;
    private final Show show;
    private volatile SeatStatus status;
    private String heldByUserId;
    private Instant holdExpiresAt;
    private String bookedByBookingId;

    private static final long HOLD_DURATION_SECONDS = 600; // 10 minutes

    public ShowSeat(Seat seat, Show show) {
        this.seat   = seat;
        this.show   = show;
        this.status = SeatStatus.AVAILABLE;
    }

    public Seat getSeat()    { return seat; }
    public Show getShow()    { return show; }

    public synchronized SeatStatus getStatus() {
        // Auto-expire held seats
        if (status == SeatStatus.HELD && Instant.now().isAfter(holdExpiresAt)) {
            status         = SeatStatus.AVAILABLE;
            heldByUserId   = null;
            holdExpiresAt  = null;
        }
        return status;
    }

    // Returns true if this thread successfully held the seat
    public synchronized boolean tryHold(String userId) {
        if (getStatus() != SeatStatus.AVAILABLE) {
            return false; // already held or booked
        }
        this.status        = SeatStatus.HELD;
        this.heldByUserId  = userId;
        this.holdExpiresAt = Instant.now().plusSeconds(HOLD_DURATION_SECONDS);
        return true;
    }

    // Returns true if the seat was successfully booked
    public synchronized boolean tryBook(String userId, String bookingId) {
        if (status != SeatStatus.HELD || !userId.equals(heldByUserId)) {
            return false;
        }
        if (Instant.now().isAfter(holdExpiresAt)) {
            status = SeatStatus.AVAILABLE;
            return false; // hold expired
        }
        this.status           = SeatStatus.BOOKED;
        this.bookedByBookingId = bookingId;
        this.heldByUserId     = null;
        this.holdExpiresAt    = null;
        return true;
    }

    public synchronized void release() {
        if (status == SeatStatus.HELD || status == SeatStatus.BOOKED) {
            status           = SeatStatus.AVAILABLE;
            heldByUserId     = null;
            holdExpiresAt    = null;
            bookedByBookingId = null;
        }
    }

    public String getHeldByUserId()       { return heldByUserId; }
    public Instant getHoldExpiresAt()     { return holdExpiresAt; }
    public String getBookedByBookingId()  { return bookedByBookingId; }
}
```

```java
// ── User ─────────────────────────────────────────────────────────────────

public class User {
    private final String userId;
    private final String name;
    private final String email;
    private final String phone;

    public User(String userId, String name, String email, String phone) {
        this.userId = userId;
        this.name   = name;
        this.email  = email;
        this.phone  = phone;
    }

    public String getUserId() { return userId; }
    public String getName()   { return name; }
    public String getEmail()  { return email; }
    public String getPhone()  { return phone; }
}
```

```java
// ── Booking ───────────────────────────────────────────────────────────────

public class Booking {
    private final String bookingId;
    private final User user;
    private final Show show;
    private final List<ShowSeat> seats;
    private BookingStatus status;
    private Payment payment;
    private final LocalDateTime createdAt;

    public Booking(User user, Show show, List<ShowSeat> seats) {
        this.bookingId = "BKG-" + System.currentTimeMillis() + "-" + user.getUserId();
        this.user      = user;
        this.show      = show;
        this.seats     = new ArrayList<>(seats);
        this.status    = BookingStatus.PENDING;
        this.createdAt = LocalDateTime.now();
    }

    public double getTotalAmount() {
        return seats.stream()
            .mapToDouble(ss -> ss.getSeat().getBasePrice())
            .sum();
    }

    public void confirm(Payment payment) {
        this.payment = payment;
        this.status  = BookingStatus.CONFIRMED;
    }

    public void cancel() {
        this.status = BookingStatus.CANCELLED;
        seats.forEach(ShowSeat::release);
    }

    public String getBookingId()         { return bookingId; }
    public User getUser()                { return user; }
    public Show getShow()                { return show; }
    public List<ShowSeat> getSeats()     { return Collections.unmodifiableList(seats); }
    public BookingStatus getStatus()     { return status; }
    public LocalDateTime getCreatedAt()  { return createdAt; }

    @Override
    public String toString() {
        return String.format("Booking{id=%s, user=%s, show=%s, seats=%d, amount=₹%.2f, status=%s}",
            bookingId, user.getName(), show.getShowId(), seats.size(), getTotalAmount(), status);
    }
}
```

```java
// ── Payment ───────────────────────────────────────────────────────────────

public class Payment {
    private final String paymentId;
    private final Booking booking;
    private final double amount;
    private final String paymentMethod; // "UPI", "CARD", "NET_BANKING"
    private final LocalDateTime paidAt;

    public Payment(Booking booking, String paymentMethod) {
        this.paymentId     = "PAY-" + System.currentTimeMillis();
        this.booking       = booking;
        this.amount        = booking.getTotalAmount();
        this.paymentMethod = paymentMethod;
        this.paidAt        = LocalDateTime.now();
    }

    public String getPaymentId()   { return paymentId; }
    public double getAmount()      { return amount; }
    public LocalDateTime getPaidAt() { return paidAt; }
}
```

```java
// ── Booking Service (The Core Business Logic) ─────────────────────────────

public class BookingService {
    private final ShowRepository showRepository;
    private final BookingRepository bookingRepository;
    private final Map<String, Booking> pendingBookings = new ConcurrentHashMap<>();

    private static final int MAX_SEATS_PER_BOOKING = 10;

    public BookingService(ShowRepository showRepository,
                          BookingRepository bookingRepository) {
        this.showRepository   = showRepository;
        this.bookingRepository = bookingRepository;
    }

    /**
     * Step 1: Hold seats — 10-minute window for the user to complete payment.
     * Returns a booking in PENDING state.
     */
    public Booking holdSeats(User user, String showId, List<String> seatIds) {
        if (seatIds.isEmpty() || seatIds.size() > MAX_SEATS_PER_BOOKING) {
            throw new IllegalArgumentException(
                "Must book between 1 and " + MAX_SEATS_PER_BOOKING + " seats");
        }

        Show show = showRepository.findById(showId)
            .orElseThrow(() -> new IllegalArgumentException("Show not found: " + showId));

        // Collect the show seats — fail fast if any seat doesn't exist
        List<ShowSeat> showSeats = seatIds.stream()
            .map(seatId -> {
                ShowSeat ss = show.getShowSeats().get(seatId);
                if (ss == null) throw new IllegalArgumentException("Invalid seat: " + seatId);
                return ss;
            })
            .collect(java.util.stream.Collectors.toList());

        // Attempt to hold ALL requested seats atomically
        // If any seat fails to hold, release all previously held seats
        List<ShowSeat> heldSeats = new ArrayList<>();
        try {
            for (ShowSeat showSeat : showSeats) {
                if (!showSeat.tryHold(user.getUserId())) {
                    throw new SeatNotAvailableException(
                        "Seat " + showSeat.getSeat().getSeatId() + " is not available");
                }
                heldSeats.add(showSeat);
            }
        } catch (SeatNotAvailableException e) {
            // Roll back — release any seats we successfully held before the failure
            heldSeats.forEach(ss -> ss.release());
            throw e;
        }

        Booking booking = new Booking(user, show, heldSeats);
        pendingBookings.put(booking.getBookingId(), booking);
        bookingRepository.save(booking);

        System.out.printf("🎫 Seats held for user %s: %s (expires in 10 min)%n",
            user.getName(), seatIds);
        return booking;
    }

    /**
     * Step 2: Confirm booking after payment succeeds.
     */
    public Booking confirmBooking(String bookingId, String paymentMethod) {
        Booking booking = pendingBookings.get(bookingId);
        if (booking == null) {
            throw new IllegalArgumentException("Booking not found: " + bookingId);
        }
        if (booking.getStatus() != BookingStatus.PENDING) {
            throw new IllegalStateException("Booking is not in PENDING state");
        }

        // Try to book all seats (will fail if hold expired)
        for (ShowSeat showSeat : booking.getSeats()) {
            if (!showSeat.tryBook(booking.getUser().getUserId(), bookingId)) {
                booking.cancel();
                pendingBookings.remove(bookingId);
                throw new IllegalStateException(
                    "Hold expired or seat " + showSeat.getSeat().getSeatId()
                    + " no longer available. Please try again.");
            }
        }

        Payment payment = new Payment(booking, paymentMethod);
        booking.confirm(payment);
        pendingBookings.remove(bookingId);
        bookingRepository.save(booking);

        System.out.printf("✅ Booking confirmed: %s%n", booking);
        return booking;
    }

    /**
     * Cancel a pending or confirmed booking.
     */
    public void cancelBooking(String bookingId) {
        Booking booking = bookingRepository.findById(bookingId)
            .orElseThrow(() -> new IllegalArgumentException("Booking not found: " + bookingId));
        booking.cancel();
        bookingRepository.save(booking);
        System.out.println("❌ Booking cancelled: " + bookingId);
    }
}
```

```java
// ── Hold Expiry: @Scheduled Job ───────────────────────────────────────────

@Component
public class SeatHoldExpiryJob {
    // In-memory approach — for production use Redis TTL or DB scheduled scan
    // This job periodically scans pending bookings and expires stale holds

    @Scheduled(fixedDelay = 60_000) // Run every 60 seconds
    public void expireStaleHolds() {
        // In a real system: query DB for bookings in PENDING state older than 10 min
        // For each: set status = EXPIRED, release ShowSeat holds
        System.out.println("[SeatHoldExpiryJob] Scanning for expired holds...");
        // SELECT * FROM bookings WHERE status='PENDING' AND created_at < NOW() - INTERVAL 10 MINUTE
    }
}
```

```java
// ── Repository Interfaces ─────────────────────────────────────────────────

public interface ShowRepository {
    Optional<Show> findById(String showId);
    List<Show> findByMovieAndCityAndDate(String movieId, String city, LocalDate date);
}

public interface BookingRepository {
    void save(Booking booking);
    Optional<Booking> findById(String bookingId);
    List<Booking> findByUserAndStatus(String userId, BookingStatus status);
}
```

```java
// ── Custom Exception ──────────────────────────────────────────────────────

public class SeatNotAvailableException extends RuntimeException {
    public SeatNotAvailableException(String message) { super(message); }
}
```

---

## Step 5: Concurrency Analysis

### Scenario: Two Users Book Seat A5 Simultaneously

```
User A: holdSeats(showId, ["A5", "A6"])
User B: holdSeats(showId, ["A5", "B1"])

Thread A → showSeat_A5.tryHold("user_A")  ← acquires synchronized lock
  → status is AVAILABLE
  → sets status = HELD, heldByUserId = "user_A"
  → returns true
  → releases lock

Thread B → showSeat_A5.tryHold("user_B")  ← acquires synchronized lock
  → status is now HELD (not AVAILABLE)
  → returns false
  → releases lock

Thread B's holdSeats() catches SeatNotAvailableException
→ releases showSeat_B1 (which was already held)
→ throws exception to the caller: "Seat A5 is not available"
```

The `synchronized` on `tryHold` is the correctness guarantee. Only one thread can check-and-set the status atomically.

### Database-Level Prevention (Production)

```sql
-- Optimistic locking: add a version column
-- If two transactions try to update the same row, one gets a version mismatch and retries
UPDATE show_seats
   SET status = 'HELD',
       held_by = :userId,
       hold_expires_at = NOW() + INTERVAL 10 MINUTE,
       version = version + 1
 WHERE seat_id = :seatId
   AND show_id = :showId
   AND status  = 'AVAILABLE'
   AND version = :currentVersion;  -- fails if another transaction updated first

-- Pessimistic locking for guaranteed safety in high-concurrency bursts:
SELECT * FROM show_seats
 WHERE seat_id = :seatId AND show_id = :showId
   FOR UPDATE;  -- locks the row; other transactions wait
```

### Redis-Based Hold (Flash Sales: 100K Concurrent Users)

```java
// Redis atomic operation: SET key value EX ttl NX
// NX = only set if Not eXists → exactly one thread wins

// In pseudocode for BookMyShow's Redis layer:
public boolean holdSeatInRedis(String showId, String seatId, String userId) {
    String redisKey = "seat:" + showId + ":" + seatId;
    // SET seat:show123:A5 user456 EX 600 NX
    // Returns OK if set, null if already exists
    String result = redisTemplate.opsForValue()
        .setIfAbsent(redisKey, userId, Duration.ofSeconds(600));
    return "OK".equals(result);
}

// Why Redis works for flash sales:
// 1. Single-threaded command execution in Redis — inherently atomic
// 2. O(1) operation — can handle 100K/sec
// 3. TTL: key auto-expires after 600 seconds — no cleanup job needed
// 4. After hold, write to DB asynchronously (CQRS pattern)
```

---

## Interview Questions

**Q: How do you prevent double booking?**

A: Three layers of defense:
1. `synchronized` on `ShowSeat.tryHold()` for in-memory safety
2. `SELECT ... FOR UPDATE` or optimistic locking with a version column in the database
3. `SET key value NX` in Redis for distributed, high-throughput scenarios

**Q: What happens if the user's browser crashes after holding but before payment?**

A: The `ShowSeat.getStatus()` auto-expires holds by checking `Instant.now().isAfter(holdExpiresAt)`. Additionally, a `@Scheduled` job scans for bookings in PENDING state older than 10 minutes and releases them. With Redis, the TTL handles this automatically at the key level.

**Q: How would you handle a flash sale with 100K concurrent users?**

A: Five-point answer:
1. **Rate limit** at the API gateway (token bucket algorithm)
2. **Queue** incoming requests in a bounded queue (Kafka/SQS) to smooth the spike
3. **Redis** for seat holds — `SET key val NX EX 600` is O(1) and atomic
4. **Pre-compute availability** and cache the seat map in Redis, not the DB
5. **Circuit breaker** on the payment service so a slow payment provider doesn't cascade

**Q: How do you design the seat layout display (the seat map UI data)?**

A: `GET /shows/{showId}/seats` returns all `ShowSeat` objects with their current status. For high traffic, cache this in Redis and invalidate when a seat changes status. The client polls every 30 seconds to update the live availability view.

**Q: What's the difference between HELD and BOOKED in your state machine?**

A: HELD is a temporary reservation during the payment window (10 minutes). If payment doesn't complete within 10 minutes, the seat returns to AVAILABLE. BOOKED is a permanent, payment-confirmed state. A seat in HELD state has an `expiry timestamp`; BOOKED seats never expire.
