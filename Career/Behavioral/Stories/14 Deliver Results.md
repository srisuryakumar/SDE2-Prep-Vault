---
type: star-story
story_id: 14
title: "Deliver Results — Angular to React Migration"
amazon_lps: ["Deliver Results"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
Our team committed to migrating our entire legacy Angular codebase to React within 3 months, a goal everyone said was too aggressive.

### Task
I was responsible for migrating the most complex piece: the multi-step checkout flow.

### Action
I broke the checkout flow into micro-frontends, allowing us to migrate one step at a time and run React inside Angular using single-spa. I strictly scoped the work, refusing feature creep, and put in focused hours. I also built a suite of Cypress end-to-end tests before touching the code to ensure parity.

### Result
I delivered the React checkout flow 1 week ahead of schedule with zero regression bugs in production, which allowed the team to hit the 3-month deadline. Conversion rates actually increased by 5% due to the improved React load times.
