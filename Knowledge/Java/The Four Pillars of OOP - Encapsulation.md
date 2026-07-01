---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, oop, encapsulation]
---

# The Four Pillars of OOP - Encapsulation

Encapsulation is the practice of bundling data (fields) with the methods that operate on that data, while hiding the internal state from the outside world.

## How it works
1. **Private Data:** Make fields `private`. This prevents external code from modifying state directly and bypassing rules.
2. **Controlled Access:** Provide `public` methods (getters, setters, or business methods like `deposit()`) to interact with the data.

## Why it matters
Encapsulation allows a class to enforce invariants (business rules). 
If a `BankAccount`'s `balance` field is public, external code can do `account.balance = -1000`. If `balance` is private and modified only via `account.deposit()` and `account.withdraw()`, the class can validate the amount, throw an exception if the funds are insufficient, and maintain a transaction log—safely guaranteeing the object remains in a valid state.
