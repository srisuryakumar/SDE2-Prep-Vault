### Naming Convention

Title Case with spaces, zero-padded numeric prefixes where an ordering exists, `.md` extension. Index/navigation notes get a leading underscore so they sort to the top of their folder and read visually as "not a content note." Examples: `Day 001.md`, `0001 Two Sum.md`, `HashMap Internals.md`, `_Java MOC.md`, `ADR 001 Why Kafka Over HTTP.md`.

### Frontmatter Schemas

Every note type gets a `type:` property. This matters more than which folder the note lives in — Dataview queries in Phase 6 mostly filter by `type`, not by folder path, so the dashboard survives future reorganization.

**Daily Note** (`Daily Journal/Day NNN.md`):
```yaml
---
type: daily-note
day_number: 1
week_number: 1
planned_date: 2026-06-16
status: planned        # planned | in-progress | complete
dsa_problems: []        # links to Practice/LeetCode notes
theory_topics: []       # links to Knowledge notes
project_repo:            # link to Practice/Projects note, if applicable
mock_today: false
tags: [daily]
---
```

**LeetCode Problem Note** (`Practice/LeetCode/NNNN Title.md`):
```yaml
---
type: leetcode-problem
leetcode_id: 1
title: Two Sum
difficulty: Easy        # Easy | Medium | Hard
patterns: []             # links to Practice/LeetCode/_Patterns notes
companies: []             # appended to, never duplicated — see Phase 2 dedup rule
status: not-started      # not-started | attempted | solved | mastered
first_solved_date:
last_reviewed:
review_count: 0
next_review_due:
avg_time_min:
tags: [leetcode]
---
```

**Knowledge Concept Note** (`Knowledge/[Subject]/Title.md`):
```yaml
---
type: concept
subject: Java
source_book: "Book 1 — Java Mastery"
source_chapter: "Chapter 5 — The Collections Framework"
status: to-study          # to-study | studied | needs-review | mastered | stub
interview_frequency: high  # high | medium | low
introduced_day:             # link back to the first Daily Note that covers this
related_concepts: []
tags: [java]
---
```

A `status: stub` value exists specifically for Phase 4 — if a Daily Note needs to link to a concept that Phase 1 didn't create, the agent creates a one-sentence stub rather than skipping the link, so nothing silently falls through the cracks. A later Dataview query in Phase 6 surfaces all stubs so you know what to flesh out.

**Company Dossier** (`Career/Companies/Name.md`):
```yaml
---
type: company-dossier
company: Razorpay
tier: A
tech_stack: []
base_salary_range: "₹45-55L"
tags: [company, tier-a]
---
```

**Application Record** (`Career/Applications/Company - Role - Date.md`):
```yaml
---
type: application
company: "[[Razorpay]]"
role: SDE-2
date_applied:
platform:
referral: false
referrer_name:
status: applied            # applied | screening | oa-sent | technical-1 | technical-2 | system-design | hm | offer | rejected | ghosted
follow_up_date:
interview_date:
outcome:
tags: [application]
---
```

This is deliberately separate from the company dossier note. The dossier is static research (tech stack, salary bands) that doesn't change often; the application record is transactional and you may have several over time for the same company.

**STAR Story** (`Career/Behavioral/Stories/NN Title.md`):
```yaml
---
type: star-story
story_id: 1
title: Customer Obsession — Dashboard Performance
amazon_lps: ["Customer Obsession"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---
```

**Mock Interview Log** (`Practice/Mocks/Date Type.md`):
```yaml
---
type: mock-interview
date:
mock_type: DSA              # DSA | LLD | System-Design | Behavioral | Full-Loop
related_day:
score:
weak_points: []
tags: [mock]
---
```

**Interview Debrief** (`Career/Interview Debriefs/Company Round Date.md`):
```yaml
---
type: interview-debrief
company: "[[Razorpay]]"
round_type: DSA              # DSA | LLD | System-Design | Behavioral | HM
date:
related_application:          # link to the Career/Applications note this round belongs to
outcome_signal:
root_cause:
reapply_eligible_date:
tags: [interview-debrief]
---
```

This is distinct from the Mock Interview Log above — mocks are practice, before interview season starts. This is for actual rounds with real companies once interviews begin (Week 15 onward in the roadmap), and links forward to a real Application record rather than just a Daily Note.

**Project Hub** (`Practice/Projects/repo-name.md`):
```yaml
---
type: project
repo_name: todo-api
start_day:
status: in-progress
tech_stack: []
github_url:
tags: [project]
---
```

**ADR** (`Practice/Projects/[repo]/ADRs/ADR NNN Title.md`):
```yaml
---
type: adr
adr_number: 1
title: Why Kafka Over HTTP Calls
status: accepted
date:
project: "[[order-management-api]]"
tags: [adr]
---
```

### Linking Conventions

Use `[[Note Name]]` for a plain link. Use `[[Note Name|display text]]` when the link should read naturally inside a sentence — e.g., "...solved using a [[0001 Two Sum|HashMap complement-counting]] approach." Use `[[Note Name#Heading]]` to link to a specific section inside a longer note, mainly for linking into specific entries within an MOC. Use frontmatter properties (not inline tags) for anything that needs to be filtered or sorted by Dataview — status, difficulty, dates. Reserve inline `#tags` for loose cross-cutting labels that don't need a value attached.
