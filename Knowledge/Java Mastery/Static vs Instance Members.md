---
type: concept
subject: Java Mastery
source_book: "Book 1 — Java Language and API Mastery"
source_chapter: "Chapter 4 — Object-Oriented Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [java, static, memory, oop]
---

# Static vs Instance Members

In Java, understanding whether a field or method belongs to the class or an instance is critical.

## Instance Members (No Keyword)
- **Fields:** Every object instantiated receives its own separate copy of the field, stored on the Heap. Modifying one object's field does not affect another object.
- **Methods:** Can access both instance and static members. They operate using the specific data of the object they were called on (via `this`).

## Static Members (`static` keyword)
- **Fields:** There is only **one shared copy** of the field, regardless of how many objects exist. It belongs to the Class itself and is stored in the Metaspace. If one instance modifies a static field, all other instances see the change.
- **Methods:** Belong to the class. They **cannot access instance fields or use `this`** because they are not tied to any specific object. They can only access other static members.

```java
public class Company {
    // Instance field
    private String name;
    
    // Static field
    private static int totalCompanies = 0;
    
    public Company(String name) {
        this.name = name;
        totalCompanies++; // Increment shared counter
    }
}
```
