---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 2 — Creational Patterns"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Abstract Factory Pattern", "Open-Closed Principle (OCP)"]
tags: [lld, design-patterns, creational]
---

# Factory Method Pattern

## Intuition
Instead of scattering `new StripeProcessor()` and `new PayPalProcessor()` throughout your business logic, you centralize object creation. The Factory Method pattern defines an interface for creating an object, but lets *subclasses* decide which class to instantiate.

## The Problem with Direct Instantiation
If your `PaymentController` creates concrete objects via `new` inside an `if/else` chain, it violates the Open-Closed Principle (OCP). Adding a new payment method means modifying the controller.

## The Solution
1. Define a `PaymentGateway` interface (the product).
2. Define a `PaymentGatewayFactory` (the creator) with an abstract `createGateway()` method.
3. Subclasses like `StripeFactory` implement `createGateway()` to return a `StripeGateway`.
4. Your business logic depends only on the Factory interface, never the concrete classes.

## Simple Factory (Interview Common)
A variation uses a static registry (a `Map<String, Supplier<PaymentGateway>>`). You register suppliers at startup, and create objects via `PaymentFactory.create("STRIPE")`. It avoids deep inheritance trees.
