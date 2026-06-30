---
type: star-story
story_id: 5
title: "Learn and Be Curious — Memory Leaks"
amazon_lps: ["Learn and Be Curious"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
Our web app was suffering from memory leaks, causing the browser tab to crash after an hour of use. Nobody on the team knew how to debug V8 memory profiles.

### Task
I needed to figure out how to find and fix the leak to stabilize the application.

### Action
I spent my weekend reading through Chrome DevTools documentation and watching advanced talks on JavaScript garbage collection. I learned how to take heap snapshots, compare them, and trace retained sizes. Back at work, I applied this technique, isolating the issue to a detached DOM node caused by an improperly destroyed third-party charting library.

### Result
I fixed the leak, wrote a wiki page on how to use the memory profiler, and hosted a 30-minute lunch-and-learn for the team. App crashes were eliminated.
