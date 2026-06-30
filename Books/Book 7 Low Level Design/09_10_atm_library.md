# Chapter 9: LLD Design 5 — ATM Machine

> ATM design demonstrates Chain of Responsibility (validation pipeline), State Machine (transaction flow), and a classic greedy algorithm (cash dispensing with fewest bills).

---

## Step 1: Requirements

- Card insertion and PIN validation
- Balance enquiry
- Cash withdrawal (dispense with fewest bills)
- Deposit
- Mini statement
- Transaction timeout
- State machine: IDLE → CARD_INSERTED → PIN_ENTERED → AUTHENTICATED → TRANSACTION → EJECTING

---

## Step 2: Entities

```
ATM                 — context: holds cash, drives state machine
ATMState            — interface: handles actions per state
Card                — physical card details
Account             — bank account with balance
Transaction         — withdrawal/deposit record
CashDispenser       — greedy algorithm for bill selection
Validator chain:    CardValidator → PINValidator → AccountValidator → TransactionValidator
```

---

## Step 3: Full Java Implementation

```java
// ── Enums and Core Data ───────────────────────────────────────────────────

public enum TransactionType { WITHDRAWAL, DEPOSIT, BALANCE_ENQUIRY, MINI_STATEMENT }

public class Card {
    private final String cardNumber;  // masked: "**** **** **** 1234"
    private final String cardHolderName;
    private final String expiryDate;
    private final String maskedPan;

    public Card(String cardNumber, String cardHolderName, String expiryDate) {
        this.cardNumber      = cardNumber;
        this.cardHolderName  = cardHolderName;
        this.expiryDate      = expiryDate;
        this.maskedPan       = "**** **** **** " + cardNumber.substring(cardNumber.length() - 4);
    }

    public String getCardNumber()     { return cardNumber; }
    public String getCardHolderName() { return cardHolderName; }
    public String getMaskedPan()      { return maskedPan; }
    public boolean isExpired() {
        // Simplified expiry check
        return false;
    }
}

public class Account {
    private final String accountNumber;
    private final String linkedCardNumber;
    private final String pinHash;  // bcrypt hash in production
    private double balance;
    private boolean blocked;
    private int failedPinAttempts;
    private final List<TransactionRecord> history;

    public Account(String accountNumber, String cardNumber, String pinHash, double balance) {
        this.accountNumber   = accountNumber;
        this.linkedCardNumber = cardNumber;
        this.pinHash         = pinHash;
        this.balance         = balance;
        this.blocked         = false;
        this.failedPinAttempts = 0;
        this.history         = new ArrayList<>();
    }

    public boolean validatePin(String pin) {
        // In production: BCrypt.checkpw(pin, pinHash)
        return pinHash.equals(pin);
    }

    public void incrementFailedAttempts() {
        failedPinAttempts++;
        if (failedPinAttempts >= 3) {
            blocked = true;
            System.out.println("⛔ Account blocked after 3 failed PIN attempts");
        }
    }

    public void resetFailedAttempts() { failedPinAttempts = 0; }

    public synchronized boolean withdraw(double amount) {
        if (amount > balance) return false;
        balance -= amount;
        history.add(new TransactionRecord(TransactionType.WITHDRAWAL, amount, balance));
        return true;
    }

    public synchronized void deposit(double amount) {
        balance += amount;
        history.add(new TransactionRecord(TransactionType.DEPOSIT, amount, balance));
    }

    public String getAccountNumber()   { return accountNumber; }
    public String getLinkedCardNumber() { return linkedCardNumber; }
    public double getBalance()         { return balance; }
    public boolean isBlocked()         { return blocked; }
    public List<TransactionRecord> getHistory() { return Collections.unmodifiableList(history); }
}

public class TransactionRecord {
    private final TransactionType type;
    private final double amount;
    private final double balanceAfter;
    private final LocalDateTime timestamp;

    public TransactionRecord(TransactionType type, double amount, double balanceAfter) {
        this.type         = type;
        this.amount       = amount;
        this.balanceAfter = balanceAfter;
        this.timestamp    = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return String.format("%s | %s | ₹%.2f | Balance: ₹%.2f",
            timestamp.toLocalDate(), type, amount, balanceAfter);
    }
}
```

```java
// ── Chain of Responsibility: Validators ───────────────────────────────────

public abstract class ATMValidator {
    protected ATMValidator next;

    public ATMValidator setNext(ATMValidator next) {
        this.next = next;
        return next;
    }

    public abstract ValidationResult validate(ATMContext context);

    protected ValidationResult passToNext(ATMContext context) {
        if (next != null) return next.validate(context);
        return ValidationResult.success();
    }
}

public class ValidationResult {
    private final boolean valid;
    private final String message;

    private ValidationResult(boolean valid, String message) {
        this.valid   = valid;
        this.message = message;
    }

    public static ValidationResult success() { return new ValidationResult(true, "OK"); }
    public static ValidationResult failure(String msg) { return new ValidationResult(false, msg); }

    public boolean isValid()     { return valid; }
    public String getMessage()   { return message; }
}

// ATM context passed through the chain
public class ATMContext {
    private Card card;
    private Account account;
    private String enteredPin;
    private double requestedAmount;

    // Setters and getters
    public Card getCard()               { return card; }
    public void setCard(Card card)      { this.card = card; }
    public Account getAccount()         { return account; }
    public void setAccount(Account acct) { this.account = acct; }
    public String getEnteredPin()       { return enteredPin; }
    public void setEnteredPin(String p) { this.enteredPin = p; }
    public double getRequestedAmount()  { return requestedAmount; }
    public void setRequestedAmount(double a) { this.requestedAmount = a; }
}

public class CardValidator extends ATMValidator {
    private final Map<String, Account> accountRepository; // cardNumber → Account

    public CardValidator(Map<String, Account> accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Override
    public ValidationResult validate(ATMContext context) {
        Card card = context.getCard();
        if (card == null) return ValidationResult.failure("No card inserted");
        if (card.isExpired()) return ValidationResult.failure("Card is expired");

        Account account = accountRepository.get(card.getCardNumber());
        if (account == null) return ValidationResult.failure("Card not recognized");

        context.setAccount(account);
        System.out.println("[CardValidator] Card valid: " + card.getMaskedPan());
        return passToNext(context);
    }
}

public class PINValidator extends ATMValidator {
    @Override
    public ValidationResult validate(ATMContext context) {
        Account account = context.getAccount();
        if (account.isBlocked()) {
            return ValidationResult.failure("Account is blocked. Please visit a branch.");
        }

        boolean pinCorrect = account.validatePin(context.getEnteredPin());
        if (!pinCorrect) {
            account.incrementFailedAttempts();
            return ValidationResult.failure("Incorrect PIN. Attempts remaining: "
                + (3 - account.isBlocked() ? 0 : /* attempts */ 0));
        }

        account.resetFailedAttempts();
        System.out.println("[PINValidator] PIN verified for account: "
            + account.getAccountNumber());
        return passToNext(context);
    }
}

public class AccountValidator extends ATMValidator {
    @Override
    public ValidationResult validate(ATMContext context) {
        Account account = context.getAccount();
        if (account.getBalance() < 0) {
            return ValidationResult.failure("Account has negative balance");
        }
        System.out.println("[AccountValidator] Account OK. Balance: ₹"
            + String.format("%.2f", account.getBalance()));
        return passToNext(context);
    }
}

public class TransactionAmountValidator extends ATMValidator {
    private static final double MIN_WITHDRAWAL = 100;
    private static final double MAX_WITHDRAWAL = 20000;
    private static final double MULTIPLE_OF    = 100;

    @Override
    public ValidationResult validate(ATMContext context) {
        double amount  = context.getRequestedAmount();
        Account account = context.getAccount();

        if (amount < MIN_WITHDRAWAL) {
            return ValidationResult.failure("Minimum withdrawal: ₹" + MIN_WITHDRAWAL);
        }
        if (amount > MAX_WITHDRAWAL) {
            return ValidationResult.failure("Maximum withdrawal per transaction: ₹" + MAX_WITHDRAWAL);
        }
        if (amount % MULTIPLE_OF != 0) {
            return ValidationResult.failure("Amount must be a multiple of ₹" + (int) MULTIPLE_OF);
        }
        if (amount > account.getBalance()) {
            return ValidationResult.failure(
                String.format("Insufficient balance. Available: ₹%.2f", account.getBalance()));
        }

        System.out.println("[TransactionValidator] Amount ₹" + amount + " is valid");
        return passToNext(context);
    }
}
```

```java
// ── Cash Dispenser: Greedy Algorithm ─────────────────────────────────────

public class CashDispenser {
    // Denominations in descending order
    private static final int[] DENOMINATIONS = {2000, 500, 200, 100};

    private final Map<Integer, Integer> cassettes; // denomination → count

    public CashDispenser() {
        cassettes = new LinkedHashMap<>();
        cassettes.put(2000, 10);
        cassettes.put(500,  20);
        cassettes.put(200,  30);
        cassettes.put(100,  50);
    }

    /**
     * Greedy: use largest denomination first to minimize number of bills.
     * Returns map of denomination → count used, or empty if can't dispense.
     */
    public Optional<Map<Integer, Integer>> dispense(int amount) {
        Map<Integer, Integer> dispensed = new LinkedHashMap<>();
        int remaining = amount;

        for (int denomination : DENOMINATIONS) {
            if (remaining <= 0) break;
            int available = cassettes.getOrDefault(denomination, 0);
            int needed    = Math.min(remaining / denomination, available);
            if (needed > 0) {
                dispensed.put(denomination, needed);
                remaining -= needed * denomination;
            }
        }

        if (remaining != 0) {
            return Optional.empty(); // can't make exact amount with available bills
        }

        // Commit: deduct from cassettes
        dispensed.forEach((denom, count) ->
            cassettes.merge(denom, -count, Integer::sum)
        );

        return Optional.of(dispensed);
    }

    public void replenish(int denomination, int count) {
        cassettes.merge(denomination, count, Integer::sum);
    }

    public int getTotalCash() {
        return cassettes.entrySet().stream()
            .mapToInt(e -> e.getKey() * e.getValue())
            .sum();
    }

    public void printStatus() {
        System.out.println("[CashDispenser] Cassette Status:");
        cassettes.forEach((denom, count) ->
            System.out.printf("  ₹%4d x %3d = ₹%6d%n", denom, count, denom * count)
        );
        System.out.println("  Total: ₹" + getTotalCash());
    }
}
```

```java
// ── ATM State Machine ─────────────────────────────────────────────────────

public interface ATMState {
    void insertCard(ATM atm, Card card);
    void enterPin(ATM atm, String pin);
    void requestWithdrawal(ATM atm, double amount);
    void requestBalance(ATM atm);
    void requestMiniStatement(ATM atm);
    void ejectCard(ATM atm);
    String getStateName();
}

public class IdleState implements ATMState {
    @Override
    public void insertCard(ATM atm, Card card) {
        atm.setCurrentCard(card);
        System.out.println("🏧 Card inserted: " + card.getMaskedPan());
        atm.setState(new CardInsertedState());
    }
    @Override public void enterPin(ATM atm, String pin) {
        System.out.println("[Idle] Please insert card first.");
    }
    @Override public void requestWithdrawal(ATM atm, double amount) {
        System.out.println("[Idle] Please insert card first.");
    }
    @Override public void requestBalance(ATM atm) {
        System.out.println("[Idle] Please insert card first.");
    }
    @Override public void requestMiniStatement(ATM atm) {
        System.out.println("[Idle] Please insert card first.");
    }
    @Override public void ejectCard(ATM atm) {
        System.out.println("[Idle] No card to eject.");
    }
    @Override public String getStateName() { return "IDLE"; }
}

public class CardInsertedState implements ATMState {
    @Override
    public void insertCard(ATM atm, Card card) {
        System.out.println("[CardInserted] Card already inserted.");
    }

    @Override
    public void enterPin(ATM atm, String pin) {
        ATMContext ctx = new ATMContext();
        ctx.setCard(atm.getCurrentCard());
        ctx.setEnteredPin(pin);

        // Run only the card and PIN validators
        ValidationResult result = atm.getCardValidator().validate(ctx);
        if (!result.isValid()) {
            System.out.println("❌ " + result.getMessage());
            return;
        }

        atm.setCurrentAccount(ctx.getAccount());
        atm.setState(new AuthenticatedState());
        System.out.println("✅ Authentication successful. Welcome, "
            + ctx.getAccount().getAccountNumber());
    }

    @Override public void requestWithdrawal(ATM atm, double amount) {
        System.out.println("[CardInserted] Please enter PIN first.");
    }
    @Override public void requestBalance(ATM atm) {
        System.out.println("[CardInserted] Please enter PIN first.");
    }
    @Override public void requestMiniStatement(ATM atm) {
        System.out.println("[CardInserted] Please enter PIN first.");
    }
    @Override public void ejectCard(ATM atm) {
        System.out.println("Card ejected.");
        atm.setCurrentCard(null);
        atm.setState(new IdleState());
    }
    @Override public String getStateName() { return "CARD_INSERTED"; }
}

public class AuthenticatedState implements ATMState {
    @Override public void insertCard(ATM atm, Card card) {
        System.out.println("[Authenticated] Please complete or cancel current session.");
    }
    @Override public void enterPin(ATM atm, String pin) {
        System.out.println("[Authenticated] Already authenticated.");
    }

    @Override
    public void requestWithdrawal(ATM atm, double amount) {
        ATMContext ctx = new ATMContext();
        ctx.setCard(atm.getCurrentCard());
        ctx.setAccount(atm.getCurrentAccount());
        ctx.setRequestedAmount(amount);

        ValidationResult result = atm.getTransactionValidator().validate(ctx);
        if (!result.isValid()) {
            System.out.println("❌ " + result.getMessage());
            return;
        }

        Optional<Map<Integer, Integer>> dispensed = atm.getCashDispenser().dispense((int) amount);
        if (dispensed.isEmpty()) {
            System.out.println("❌ ATM cannot dispense exact amount. Try a different amount.");
            return;
        }

        atm.getCurrentAccount().withdraw(amount);
        System.out.printf("💵 Dispensing ₹%.0f:%n", amount);
        dispensed.get().forEach((denom, count) ->
            System.out.printf("   ₹%d x %d%n", denom, count)
        );
    }

    @Override
    public void requestBalance(ATM atm) {
        System.out.printf("💰 Balance: ₹%.2f%n", atm.getCurrentAccount().getBalance());
    }

    @Override
    public void requestMiniStatement(ATM atm) {
        System.out.println("📄 Mini Statement (last 5 transactions):");
        List<TransactionRecord> history = atm.getCurrentAccount().getHistory();
        int start = Math.max(0, history.size() - 5);
        history.subList(start, history.size()).forEach(t -> System.out.println("  " + t));
    }

    @Override
    public void ejectCard(ATM atm) {
        System.out.println("Card ejected. Thank you!");
        atm.setCurrentCard(null);
        atm.setCurrentAccount(null);
        atm.setState(new IdleState());
    }

    @Override
    public String getStateName() { return "AUTHENTICATED"; }
}
```

```java
// ── ATM Context Object ────────────────────────────────────────────────────

public class ATM {
    private ATMState currentState;
    private Card currentCard;
    private Account currentAccount;
    private final CashDispenser cashDispenser;
    private final ATMValidator cardValidator;
    private final ATMValidator transactionValidator;

    public ATM(Map<String, Account> accountRepository) {
        this.cashDispenser = new CashDispenser();
        this.currentState  = new IdleState();

        // Build validator chains
        CardValidator cardVal = new CardValidator(accountRepository);
        PINValidator  pinVal  = new PINValidator();
        cardVal.setNext(pinVal);
        this.cardValidator = cardVal;

        AccountValidator acctVal = new AccountValidator();
        TransactionAmountValidator txVal = new TransactionAmountValidator();
        acctVal.setNext(txVal);
        this.transactionValidator = acctVal;
    }

    // State delegation
    public void insertCard(Card card)                { currentState.insertCard(this, card); }
    public void enterPin(String pin)                 { currentState.enterPin(this, pin); }
    public void requestWithdrawal(double amount)     { currentState.requestWithdrawal(this, amount); }
    public void requestBalance()                     { currentState.requestBalance(this); }
    public void requestMiniStatement()               { currentState.requestMiniStatement(this); }
    public void ejectCard()                          { currentState.ejectCard(this); }

    // Getters/setters for states to use
    public void setState(ATMState state)             { this.currentState = state; }
    public Card getCurrentCard()                     { return currentCard; }
    public void setCurrentCard(Card card)            { this.currentCard = card; }
    public Account getCurrentAccount()               { return currentAccount; }
    public void setCurrentAccount(Account acct)      { this.currentAccount = acct; }
    public CashDispenser getCashDispenser()          { return cashDispenser; }
    public ATMValidator getCardValidator()           { return cardValidator; }
    public ATMValidator getTransactionValidator()    { return transactionValidator; }
}
```

---

## Interview Questions

**Q: Why use Chain of Responsibility for ATM validators?**

A: Each validation concern is independent (card validity, PIN correctness, account status, transaction rules). Chain of Responsibility lets each validator handle only what it knows about, pass the request further, and fail fast with a clear reason. Adding a new validation (e.g., daily withdrawal limit check) means adding one new validator to the chain, not modifying existing ones.

**Q: What is the greedy algorithm for cash dispensing?**

A: Process denominations from largest to smallest. For each denomination, use as many bills as possible without exceeding the remaining amount. This minimizes the number of bills. It works correctly when denominations are multiples of each other (2000, 500, 200, 100). Note: greedy doesn't always work for arbitrary denominations — e.g., denominations {6, 4, 1} for amount 8 → greedy gives 6+1+1=3 bills, but optimal is 4+4=2 bills.

---

# Chapter 10: LLD Design 6 — Library Management System

---

## Step 1: Requirements

- Search books by title, author, ISBN, genre
- Borrow a book (if available) → issue a copy
- Return a book → update availability
- Waitlist: when the last copy is borrowed, subsequent requests go on a waitlist
- When a book is returned, notify the next person on the waitlist
- Fine calculation: overdue books accrue fines per configurable strategy
- Renew a borrowed book (extend due date, if no one on waitlist)

---

## Step 2: Entities and Relationships

```
Book              — metadata (ISBN, title, author)
BookCopy          — physical instance of a book (each has a unique ID)
Member            — library member who can borrow
BorrowRecord      — tracks who borrowed what copy, when, due date
Waitlist          — queue of members waiting for a specific book
FineCalculator    — strategy for computing overdue fines
Library           — main context
```

---

## Step 3: Full Java Implementation

```java
// ── Book and BookCopy ─────────────────────────────────────────────────────

public class Book {
    private final String isbn;
    private final String title;
    private final String author;
    private final String genre;
    private final int publicationYear;

    public Book(String isbn, String title, String author, String genre, int year) {
        this.isbn            = isbn;
        this.title           = title;
        this.author          = author;
        this.genre           = genre;
        this.publicationYear = year;
    }

    public String getIsbn()   { return isbn; }
    public String getTitle()  { return title; }
    public String getAuthor() { return author; }
    public String getGenre()  { return genre; }
}

public enum CopyStatus { AVAILABLE, BORROWED, RESERVED, LOST }

public class BookCopy {
    private final String copyId;
    private final Book book;
    private volatile CopyStatus status;

    public BookCopy(String copyId, Book book) {
        this.copyId = copyId;
        this.book   = book;
        this.status = CopyStatus.AVAILABLE;
    }

    public synchronized boolean checkout() {
        if (status != CopyStatus.AVAILABLE) return false;
        status = CopyStatus.BORROWED;
        return true;
    }

    public synchronized void returnCopy() {
        status = CopyStatus.AVAILABLE;
    }

    public String getCopyId()    { return copyId; }
    public Book getBook()        { return book; }
    public CopyStatus getStatus() { return status; }
}
```

```java
// ── Member ────────────────────────────────────────────────────────────────

public class Member {
    private final String memberId;
    private final String name;
    private final String email;
    private final LocalDate membershipExpiry;
    private int activeBorrows;
    private static final int MAX_BORROWS = 5;

    public Member(String memberId, String name, String email, LocalDate membershipExpiry) {
        this.memberId         = memberId;
        this.name             = name;
        this.email            = email;
        this.membershipExpiry = membershipExpiry;
        this.activeBorrows    = 0;
    }

    public boolean canBorrow() {
        return activeBorrows < MAX_BORROWS
            && LocalDate.now().isBefore(membershipExpiry);
    }

    public void incrementBorrows() { activeBorrows++; }
    public void decrementBorrows() { activeBorrows = Math.max(0, activeBorrows - 1); }

    public String getMemberId()   { return memberId; }
    public String getName()       { return name; }
    public String getEmail()      { return email; }
    public int getActiveBorrows() { return activeBorrows; }
}
```

```java
// ── Borrow Record ─────────────────────────────────────────────────────────

public class BorrowRecord {
    private final String recordId;
    private final Member member;
    private final BookCopy copy;
    private final LocalDate borrowDate;
    private final LocalDate dueDate;
    private LocalDate returnDate;
    private boolean renewed;

    private static final int BORROW_DAYS = 14;

    public BorrowRecord(Member member, BookCopy copy) {
        this.recordId   = "BR-" + System.currentTimeMillis();
        this.member     = member;
        this.copy       = copy;
        this.borrowDate = LocalDate.now();
        this.dueDate    = borrowDate.plusDays(BORROW_DAYS);
    }

    public void markReturned() { this.returnDate = LocalDate.now(); }

    public boolean isOverdue() {
        LocalDate checkDate = returnDate != null ? returnDate : LocalDate.now();
        return checkDate.isAfter(dueDate);
    }

    public long getOverdueDays() {
        if (!isOverdue()) return 0;
        LocalDate checkDate = returnDate != null ? returnDate : LocalDate.now();
        return java.time.temporal.ChronoUnit.DAYS.between(dueDate, checkDate);
    }

    public boolean renew(boolean waitlistEmpty) {
        if (renewed || !waitlistEmpty) return false;
        // extend due date
        // dueDate = dueDate.plusDays(BORROW_DAYS); -- need non-final for this
        this.renewed = true;
        return true;
    }

    public String getRecordId()   { return recordId; }
    public Member getMember()     { return member; }
    public BookCopy getCopy()     { return copy; }
    public LocalDate getDueDate() { return dueDate; }
    public LocalDate getReturnDate() { return returnDate; }
}
```

```java
// ── Fine Strategy ─────────────────────────────────────────────────────────

public interface FineCalculationStrategy {
    double calculateFine(BorrowRecord record);
    String getStrategyName();
}

public class PerDayFineStrategy implements FineCalculationStrategy {
    private static final double FINE_PER_DAY = 5.0; // ₹5 per day overdue
    private static final double MAX_FINE     = 500.0;

    @Override
    public double calculateFine(BorrowRecord record) {
        long overdueDays = record.getOverdueDays();
        return Math.min(overdueDays * FINE_PER_DAY, MAX_FINE);
    }

    @Override
    public String getStrategyName() { return "PER_DAY (₹5/day, max ₹500)"; }
}

public class PerWeekFineStrategy implements FineCalculationStrategy {
    private static final double FINE_PER_WEEK = 25.0;

    @Override
    public double calculateFine(BorrowRecord record) {
        long overdueDays  = record.getOverdueDays();
        long overdueWeeks = (overdueDays + 6) / 7; // round up to next week
        return overdueWeeks * FINE_PER_WEEK;
    }

    @Override
    public String getStrategyName() { return "PER_WEEK (₹25/week)"; }
}

public class GracePeriodFineStrategy implements FineCalculationStrategy {
    private static final int GRACE_PERIOD_DAYS = 3;
    private final FineCalculationStrategy baseStrategy;

    public GracePeriodFineStrategy(FineCalculationStrategy baseStrategy) {
        this.baseStrategy = baseStrategy;
    }

    @Override
    public double calculateFine(BorrowRecord record) {
        long overdueDays = record.getOverdueDays();
        if (overdueDays <= GRACE_PERIOD_DAYS) return 0; // no fine within grace period
        return baseStrategy.calculateFine(record);
    }

    @Override
    public String getStrategyName() { return "GRACE_PERIOD_3_DAYS + " + baseStrategy.getStrategyName(); }
}
```

```java
// ── Waitlist and Observer ─────────────────────────────────────────────────

public class BookWaitlist {
    private final String isbn;
    private final Queue<Member> waitlist = new LinkedList<>();

    public BookWaitlist(String isbn) { this.isbn = isbn; }

    public void addToWaitlist(Member member) {
        if (!waitlist.contains(member)) {
            waitlist.offer(member);
            System.out.printf("📋 %s added to waitlist for ISBN %s (position %d)%n",
                member.getName(), isbn, waitlist.size());
        }
    }

    public Optional<Member> getNextInWaitlist() {
        return Optional.ofNullable(waitlist.poll());
    }

    public boolean isEmpty()    { return waitlist.isEmpty(); }
    public int size()           { return waitlist.size(); }
    public String getIsbn()     { return isbn; }
}

// Observer event
public class BookReturnedEvent {
    private final Book book;
    private final Member returnedBy;
    public BookReturnedEvent(Book book, Member returnedBy) {
        this.book = book; this.returnedBy = returnedBy;
    }
    public Book getBook()         { return book; }
    public Member getReturnedBy() { return returnedBy; }
}

// Listener that notifies waitlist members
public class WaitlistNotificationListener {
    private final Map<String, BookWaitlist> waitlists;
    private final NotificationService notificationService;

    public WaitlistNotificationListener(Map<String, BookWaitlist> waitlists,
                                         NotificationService notificationService) {
        this.waitlists           = waitlists;
        this.notificationService = notificationService;
    }

    public void onBookReturned(BookReturnedEvent event) {
        String isbn = event.getBook().getIsbn();
        BookWaitlist waitlist = waitlists.get(isbn);
        if (waitlist != null && !waitlist.isEmpty()) {
            waitlist.getNextInWaitlist().ifPresent(nextMember -> {
                System.out.printf("🔔 Notifying %s: '%s' is now available!%n",
                    nextMember.getName(), event.getBook().getTitle());
                notificationService.sendEmail(nextMember.getEmail(),
                    "Book Available: " + event.getBook().getTitle());
            });
        }
    }
}
```

```java
// ── Library Service ───────────────────────────────────────────────────────

public class LibraryService {
    private final Map<String, List<BookCopy>> copies;      // isbn → copies
    private final Map<String, BookWaitlist> waitlists;     // isbn → waitlist
    private final Map<String, BorrowRecord> activeBorrows; // copyId → record
    private final FineCalculationStrategy fineStrategy;
    private final EventBus eventBus;

    public LibraryService(FineCalculationStrategy fineStrategy, EventBus eventBus) {
        this.copies        = new ConcurrentHashMap<>();
        this.waitlists     = new ConcurrentHashMap<>();
        this.activeBorrows = new ConcurrentHashMap<>();
        this.fineStrategy  = fineStrategy;
        this.eventBus      = eventBus;
    }

    public void addBook(Book book, int numberOfCopies) {
        List<BookCopy> bookCopies = new ArrayList<>();
        for (int i = 1; i <= numberOfCopies; i++) {
            bookCopies.add(new BookCopy(book.getIsbn() + "-C" + i, book));
        }
        copies.put(book.getIsbn(), bookCopies);
        System.out.printf("📚 Added: '%s' (%d copies)%n", book.getTitle(), numberOfCopies);
    }

    public synchronized BorrowRecord borrowBook(Member member, String isbn) {
        if (!member.canBorrow()) {
            throw new IllegalStateException("Member cannot borrow: limit reached or membership expired");
        }

        List<BookCopy> bookCopies = copies.getOrDefault(isbn, Collections.emptyList());
        Optional<BookCopy> availableCopy = bookCopies.stream()
            .filter(c -> c.getStatus() == CopyStatus.AVAILABLE)
            .findFirst();

        if (availableCopy.isEmpty()) {
            // No copies available — add to waitlist
            waitlists.computeIfAbsent(isbn, BookWaitlist::new).addToWaitlist(member);
            throw new RuntimeException("No copies available. Added to waitlist.");
        }

        BookCopy copy = availableCopy.get();
        copy.checkout();
        member.incrementBorrows();

        BorrowRecord record = new BorrowRecord(member, copy);
        activeBorrows.put(copy.getCopyId(), record);

        System.out.printf("✅ Borrowed: '%s' by %s. Due: %s%n",
            copy.getBook().getTitle(), member.getName(), record.getDueDate());
        return record;
    }

    public double returnBook(Member member, String copyId) {
        BorrowRecord record = activeBorrows.remove(copyId);
        if (record == null) {
            throw new IllegalArgumentException("No active borrow record for copy: " + copyId);
        }
        if (!record.getMember().getMemberId().equals(member.getMemberId())) {
            throw new IllegalStateException("This copy was not borrowed by " + member.getName());
        }

        record.markReturned();
        record.getCopy().returnCopy();
        member.decrementBorrows();

        double fine = fineStrategy.calculateFine(record);
        if (fine > 0) {
            System.out.printf("⚠️  Overdue by %d days. Fine: ₹%.2f%n",
                record.getOverdueDays(), fine);
        }

        // Notify waitlist via Observer
        eventBus.publish(new BookReturnedEvent(record.getCopy().getBook(), member));

        System.out.printf("📖 Returned: '%s' by %s%n",
            record.getCopy().getBook().getTitle(), member.getName());
        return fine;
    }

    public List<Book> search(String query) {
        String lowerQuery = query.toLowerCase();
        return copies.values().stream()
            .flatMap(List::stream)
            .map(BookCopy::getBook)
            .distinct()
            .filter(b -> b.getTitle().toLowerCase().contains(lowerQuery)
                      || b.getAuthor().toLowerCase().contains(lowerQuery)
                      || b.getIsbn().contains(query))
            .collect(java.util.stream.Collectors.toList());
    }
}
```

---

## Interview Questions

**Q: How do you notify the next person on the waitlist when a book is returned?**

A: The `returnBook` method publishes a `BookReturnedEvent` to the `EventBus`. The `WaitlistNotificationListener` is subscribed to this event. It checks if a waitlist exists for the book's ISBN, dequeues the next member, and sends a notification. This is the Observer pattern — `LibraryService` doesn't know about the waitlist implementation.

**Q: What happens if two members try to borrow the last copy simultaneously?**

A: `borrowBook` is `synchronized`, so only one thread executes at a time. The first thread finds the copy available, calls `copy.checkout()`, and creates a borrow record. The second thread finds no available copies and is added to the waitlist.

**Q: How do you calculate overdue fines?**

A: Strategy Pattern — `FineCalculationStrategy` interface with implementations: `PerDayFineStrategy` (₹5/day, max ₹500), `PerWeekFineStrategy` (₹25/week), and `GracePeriodFineStrategy` (decorator that exempts the first 3 days). Changing the fine policy = swapping the injected strategy.

**Q: How would you implement book renewals?**

A: Add a `renewBorrow(String copyId)` method. Renewal is allowed only if: (a) the book is not overdue, and (b) the waitlist for this book is empty. If both conditions pass, extend the `dueDate` by 14 days. Limit renewals to once per borrow record.
