---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 1 — OOP Design Principles Review"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Single Responsibility Principle (SRP)"]
tags: [oop, solid, design-principles]
---

# Open-Closed Principle (OCP)

## Intuition
Software entities should be **open for extension but closed for modification**.
You should be able to add new functionality (extend) without touching existing, tested code (modify).

## The Classic Violation
A massive `if-else` or `switch` chain inside a `PaymentProcessor`:
```java
if (type.equals("STRIPE")) { ... }
else if (type.equals("PAYPAL")) { ... }
```
Every time a new payment provider is added (e.g., Razorpay), you have to open and modify this core class, risking breaking Stripe and PayPal.

## The Fix
Rely on abstractions and polymorphism.
1. Define a `PaymentGateway` interface.
2. The `PaymentProcessor` accepts any object implementing `PaymentGateway` and calls `.process()`.
3. To add Razorpay, you create a *new file* (`RazorpayGateway.java`) implementing the interface. The `PaymentProcessor` is never modified.
