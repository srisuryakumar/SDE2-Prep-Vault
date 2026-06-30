---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming (OOP)"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, solid, dip]
---

# SOLID Principles - Dependency Inversion Principle

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**
Depend on interfaces, not concrete classes.

## The Violation
Hardcoding a dependency on a concrete class makes your code tightly coupled, impossible to swap out, and impossible to unit test.
```java
class OrderService {
    // Hard dependency on concrete class. Cannot swap DBs, cannot mock in tests.
    private MySQLOrderRepository repo = new MySQLOrderRepository();
    
    public void save(Order order) { repo.save(order); }
}
```

## The Fix
Depend on an interface, and inject the concrete implementation (Dependency Injection).
```java
interface OrderRepository { void save(Order order); }

class OrderService {
    private final OrderRepository repo;
    
    // Inject the dependency via constructor
    public OrderService(OrderRepository repo) {
        this.repo = repo;
    }
    
    public void save(Order order) { repo.save(order); }
}

// In production:
new OrderService(new MySQLOrderRepository());

// In tests:
new OrderService(new InMemoryOrderRepository());
```
