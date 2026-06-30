---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [spring, jpa, database, associations]
---

# JPA Associations (OneToMany, ManyToOne, OneToOne)

## Intuition
JPA defines relationships between entities. Understanding which side "owns" the relationship is critical to avoid generating duplicate join tables.

## 1. @ManyToOne
This is ALWAYS the side that holds the actual foreign key column in the database (e.g. `order_id` in the `order_items` table).
```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "order_id", nullable = false)
private Order order;
```
It is the most common and efficient association to navigate.

## 2. @OneToMany (mappedBy)
This is the *inverse* side of the `@ManyToOne` relationship.
```java
@OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
private List<OrderItem> items = new ArrayList<>();
```
- **`mappedBy = "order"`:** Tells Hibernate "Don't create a second foreign key or a join table for this. The `order` field on `OrderItem` already owns it; I am just exposing the reverse navigation."
- **Interview Trap:** If you forget `mappedBy`, Hibernate assumes `Order` owns an independent collection and silently creates a useless join table (e.g., `order_order_items`) to track the association, leading to disconnected state bugs where changes aren't persisted properly.
- **`cascade = CascadeType.ALL`:** Persist, update, and delete operations on the `Order` cascade to its `OrderItem`s. 
- **`orphanRemoval = true`:** Removing an item from the `items` list automatically deletes it from the database, because an `OrderItem` has no independent existence outside its parent.

## 3. @OneToOne
Mapped similarly, with one side owning the `@JoinColumn` and the other side using `mappedBy`.
