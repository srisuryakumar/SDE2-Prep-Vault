---
type: star-story
story_id: 16
title: "Success and Scale Bring Broad Responsibility — Accessibility"
amazon_lps: ["Success and Scale Bring Broad Responsibility"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
We were building a new onboarding flow, and the design used light grey text on a white background, which failed WCAG contrast standards.

### Task
As an engineer, I felt a responsibility to ensure our product was accessible to visually impaired users, even though accessibility wasn't explicitly in the requirements.

### Action
I pushed back on the design team, using a contrast checker to prove the colors were inaccessible. When they resisted changing the brand aesthetic, I researched and presented an alternative palette that maintained the brand identity but passed the AA accessibility standards. I also added axe-core to our CI pipeline to automatically fail PRs that introduced accessibility violations.

### Result
The design was updated. We avoided alienating visually impaired users, and accessibility became a baked-in standard for our engineering process rather than an afterthought.
