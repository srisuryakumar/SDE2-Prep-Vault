---
type: linkedin-post
post_number: 2
scheduled_week: 1
scheduled_day: Friday
status: drafted
---
Java Integer trap that would have caused a production bug.

Integer a = 127; Integer b = 127;
a == b → true ✓

Integer c = 128; Integer d = 128;
c == d → false ✗

Same logic. Different result. Why?

Java caches Integer objects between -128 and 127.
Within that range: a and b point to the SAME cached object.
Outside it: two different objects are created.

== compares object references, not values.
So c == d returns false — two different objects holding the same value.

The fix: always use .equals() for Integer comparison.
Or better: use int (primitive), where == always compares values.

Discovered this on Day 2. Going deeper into JVM memory model tomorrow.

#Java #BackendEngineering #LearningInPublic
