---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 2 — Creational Patterns"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Factory Method Pattern"]
tags: [lld, design-patterns, creational]
---

# Abstract Factory Pattern

## Intuition
Abstract Factory is Factory Method taken one level higher. Instead of creating *one* type of object, it creates a **family of related objects** that must be used together.

## The Problem
Imagine a UI toolkit. If you mix a Windows Button with a macOS Checkbox, visual consistency breaks. You need to guarantee that the UI components instantiated belong to the same family.

## The Solution
1. Define abstract products: `Button`, `Checkbox`.
2. Define an Abstract Factory: `GUIFactory` with `createButton()` and `createCheckbox()`.
3. Create concrete factories for each family: `WindowsFactory` returns `WindowsButton` and `WindowsCheckbox`. `MacOSFactory` returns the macOS equivalents.
4. The client receives a `GUIFactory` at runtime. A `MacOSFactory` will *never* accidentally produce a Windows checkbox.

**Factory Method vs Abstract Factory:**
- Factory Method: Creates ONE product, subclasses decide the type.
- Abstract Factory: Creates a FAMILY of products, ensuring compatibility.
