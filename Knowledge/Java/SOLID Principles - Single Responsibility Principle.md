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

# SOLID Principles - Single Responsibility Principle

The **S** in SOLID stands for the **Single Responsibility Principle (SRP)**.

## The Rule
A class should have **one, and only one, reason to change**. In other words, a class should only have one job.

## Example of a Violation
An `OrderService` class that handles:
1. Validating the order logic.
2. Saving the order to the database (SQL execution).
3. Sending a confirmation email.
4. Generating a PDF invoice.

If the email API changes, the PDF library updates, or the database schema is modified, this single class has to be altered. It has four reasons to change.

## The Fix
Delegate responsibilities to specialized classes.
- `OrderService` handles the business logic.
- `OrderRepository` handles database persistence.
- `NotificationService` handles emails.
- `InvoiceService` handles PDFs.
The `OrderService` orchestrates these dependencies rather than implementing the details itself.
