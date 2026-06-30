---
type: linkedin-post
post_number: 13
scheduled_week: 7
scheduled_day: Tuesday
status: drafted
---
4 rate limiting algorithms. Each has a different trade-off.

[ATTACH: Comparison diagram]

Fixed Window:
- Simple: increment counter, reset every minute
- Problem: burst at window boundary (180 req in 2 seconds across reset)

Sliding Window Log:
- Accurate: store timestamp of every request, count within window
- Problem: memory grows linearly with request count

Sliding Window Counter:
- Hybrid: blend current + previous window counts
- Formula: count = current_window + previous_window × (1 - elapsed%)
- Best accuracy/memory balance. What I use in production.

Token Bucket:
- Tokens added at constant rate, consumed per request
- Allows controlled bursts up to bucket size
- Used by AWS API Gateway and most cloud providers

For distributed rate limiting:
All of these need Redis to share state across instances.
The sliding window counter maps cleanly to Redis INCR + EXPIRE.

#DistributedSystems #BackendEngineering #SystemDesign
