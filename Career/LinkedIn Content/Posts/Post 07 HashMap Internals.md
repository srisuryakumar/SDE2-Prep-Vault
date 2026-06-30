---
type: linkedin-post
post_number: 7
scheduled_week: 4
scheduled_day: Tuesday
status: drafted
---
HashMap is not just a key-value store. Here's what happens under the hood.

[ATTACH: ASCII or Canva diagram of HashMap bucket array]

Step 1: key.hashCode() is called
Step 2: The hash is XOR-shifted: hash ^ (hash >>> 16)
        (This spreads high bits into low bits to reduce clustering)
Step 3: Bucket index = hash & (capacity - 1)
        (Bitwise AND works because capacity is always a power of 2)
Step 4: Collision? → Linked list in bucket
        > 8 entries in one bucket? → Converts to a Red-Black tree

Resize rule: when size > capacity × 0.75, double and rehash everything.

Why this matters for interviews:
"Why do you always override hashCode() with equals()?"
→ Because equal objects MUST have equal hashCodes. Break this contract
and your object becomes impossible to find in the map.

#Java #DataStructures #BackendEngineering
