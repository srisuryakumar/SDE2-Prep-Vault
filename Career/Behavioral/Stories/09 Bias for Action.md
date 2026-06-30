---
type: star-story
story_id: 9
title: "Bias for Action — API Outage"
amazon_lps: ["Bias for Action"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
During a critical sales demo, a third-party API we relied on for currency conversion went down, breaking the pricing page.

### Task
We needed an immediate fix so the sales team could continue their calls, but the backend team was unreachable in a meeting.

### Action
I didn't wait for permission. I quickly wrote a hard-coded fallback map of the previous day's exchange rates in the frontend utility file, wrapped the failing API call in a try-catch block, and deployed a hotfix directly to production within 15 minutes.

### Result
The sales team successfully completed their demos. Afterwards, I worked with the backend team to implement a proper Redis-backed fallback cache, turning a quick hack into a robust architectural pattern.
