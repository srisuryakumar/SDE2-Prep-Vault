---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 2 — JVM Memory Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, memory, pass-by-value]
---

# Object References vs Primitive Values

In Java, understanding how memory is handled dictates how you think about variables.

## Pass-by-Value
Java passes **everything by value** — always.
- **Primitives:** The value itself (e.g., `42`) is copied.
- **Objects:** The *reference* (the memory address pointing to the Heap) is copied.

## What this means in practice
```java
Order o1 = new Order(); // o1 holds a REFERENCE to the Heap object
Order o2 = o1;          // o2 holds a COPY of the REFERENCE (same address)

o2.setQuantity(5);      // Mutates the object on the Heap
System.out.println(o1.getQuantity()); // Prints 5 (Aliasing)
```

If you pass an object to a method, the method receives a copy of the reference. It cannot reassign the caller's variable to a new object, but it *can* mutate the existing object on the Heap through that reference.

```java
void modify(Order order) {
    order.setQuantity(999); // This mutates the original object!
}

void swap(Order a, Order b) {
    Order temp = a; a = b; b = temp; 
    // Does NOTHING to the caller's variables! It only swaps local copies.
}
```
