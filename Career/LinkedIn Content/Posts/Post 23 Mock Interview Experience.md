---
type: linkedin-post
post_number: 23
scheduled_week: 12
scheduled_day: Tuesday
status: drafted
---
Did my first full SDE-2 mock interview this week. Here's the honest debrief.

Round: System Design — Design a Notification System

What I did well:
✅ Started with requirements before drawing anything (2 min)
✅ Did capacity estimation before the architecture (1000 notifications/sec → Redis DLQ)
✅ Covered multi-channel (push, email, SMS, in-app)
✅ Explained the Kafka priority queue approach clearly

What I got wrong:
❌ Forgot deduplication entirely (the interviewer had to prompt me)
❌ Did not mention retry logic or dead letter queues until asked
❌ Ran out of time on observability — never covered monitoring

What I'm fixing this week:
- Practising the 5-step framework with strict timers
- Adding deduplication (Redis SET + idempotency key) to every design
- Always covering observability in the last 5 minutes

Scores from my accountability partner: 6.5/10 overall.
Aiming for 8/10 before I sit a real interview.

#SystemDesign #InterviewPrep #BackendEngineering
