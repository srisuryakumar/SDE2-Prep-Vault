---
type: star-story
story_id: 4
title: "Are Right, A Lot — State Management Migration"
amazon_lps: ["Are Right, A Lot"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
We were tasked with migrating our frontend state management from Redux to Context API because a senior developer felt Redux was "too much boilerplate."

### Task
I had to evaluate if this migration was actually the right move for our highly complex, frequently updating dashboard.

### Action
I built a quick prototype of our heaviest component using Context API and ran React Profiler. I gathered hard data showing that Context caused unnecessary re-renders across the entire component tree because it lacked Redux's fine-grained selector optimizations. I presented this data to the team, demonstrating that while boilerplate would decrease, performance would severely degrade.

### Result
I convinced the team to stay with Redux but introduced Redux Toolkit, which eliminated the boilerplate while keeping the performance benefits. Relying on data over opinions saved us from a disastrous architectural downgrade.
