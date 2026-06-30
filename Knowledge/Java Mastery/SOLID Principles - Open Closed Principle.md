---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, solid, design]
---

# SOLID Principles - Open Closed Principle

The **O** in SOLID stands for the **Open/Closed Principle (OCP)**.

## The Rule
Software entities (classes, modules, functions) should be **open for extension, but closed for modification**.
You should be able to add new behavior to a system by writing *new* code, not by altering *existing* code.

## Example of a Violation
A `PaymentProcessor` class with a massive `if/else` block:
```java
if (type.equals("CREDIT_CARD")) { ... }
else if (type.equals("PAYPAL")) { ... }
```
To add "CRYPTO" payments, you must modify this existing class, risking breaking the existing logic.

## The Fix
Define an abstraction (e.g., `PaymentStrategy` interface). 
Create new classes for each payment type (`CreditCardStrategy`, `PaypalStrategy`, `CryptoStrategy`). The `PaymentProcessor` accepts the interface. Now, to add a new payment type, you just create a new class—the existing `PaymentProcessor` code remains untouched.
