# Progress Overview

## 120-Day Challenge Progress
```dataview
TABLE length(rows) as "Completed Days", "120" as "Total Days"
FROM "Daily Journal"
WHERE type = "daily-note" AND status = "complete"
GROUP BY true
```

## Knowledge Base Status
```dataview
TABLE length(rows) as "Count"
FROM "Knowledge"
WHERE type = "concept"
GROUP BY status
```

## Stubs (Needs Expansion)
*(Surfacing stubs here specifically so incomplete linking from Phase 4 doesn't get forgotten)*
```dataview
TABLE subject, interview_frequency
FROM "Knowledge"
WHERE type = "concept" AND status = "stub"
```

## LinkedIn Content Engine
```dataview
TABLE length(rows) as "Published", "34" as "Goal"
FROM "Career/LinkedIn Content"
WHERE type = "linkedin-post" AND status = "published"
GROUP BY true
```
